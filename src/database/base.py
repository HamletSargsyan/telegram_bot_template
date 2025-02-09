from dataclasses import dataclass, field, fields
from typing import Any, ClassVar, Self

from bson import Int64, ObjectId
from dacite import from_dict as _from_dict
from dacite.data import Data
from pymongo import AsyncMongoClient, MongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.collection import Collection

from config import config
from consts import EMPTY_OBJECTID
from datatypes import ModelSettings
from helpers.exceptions import AlreadyExists, NoResult

_client_options = {
    "host": config.database.url,
    "tz_aware": True,
}

sync_client = MongoClient(**_client_options)
async_client = AsyncMongoClient(**_client_options)

sync_db = sync_client.get_database(config.database.name)
async_db = async_client.get_database(config.database.name)

if config.general.debug and config.database.name == "dev":
    choice = input(f"Drop database `{config.database.name}`? [N/y] ")
    if choice == "y":
        sync_client.drop_database(config.database.name)
        del choice


@dataclass
class BaseModel:
    oid: ObjectId = field(init=False, metadata={"alias": "_id"})

    __settings__: ClassVar[ModelSettings]
    sync_collection: ClassVar[Collection]
    async_collection: ClassVar[AsyncCollection]

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for field_ in fields(self):
            if isinstance(getattr(type(self), field_.name, None), property):
                continue
            key = field_.metadata.get("alias", field_.name)
            value = getattr(self, field_.name)

            if isinstance(value, bool):
                result[key] = value
            elif isinstance(value, int):
                result[key] = Int64(value)
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, dict_data: Data) -> Self:
        init_data = {}
        for field_ in fields(cls):
            if isinstance(getattr(type(cls), field_.name, None), property):
                continue
            alias = field_.metadata.get("alias", field_.name)
            if alias in dict_data:
                init_data[field_.name] = dict_data[alias]
            elif field_.name in dict_data:
                init_data[field_.name] = dict_data[field_.name]
        return _from_dict(cls, init_data)

    def __post_init__(self):
        if not hasattr(self, "oid"):
            self.oid = EMPTY_OBJECTID
        self._setup_model()

    @classmethod
    def _setup_model(cls):
        if not hasattr(cls, "sync_collection"):
            cls.sync_collection = sync_db.get_collection(cls.__settings__["collection_name"])
        if not hasattr(cls, "async_collection"):
            cls.async_collection = async_db.get_collection(cls.__settings__["collection_name"])

    @classmethod
    def _handle_options(cls, options: dict[str, Any]) -> dict[str, Any]:
        return options

    @classmethod
    def get(cls, **options) -> Self:
        cls._setup_model()
        options = cls._handle_options(options)
        obj = cls.sync_collection.find_one(options)

        if not obj:
            raise NoResult
        return cls.from_dict(obj)

    @classmethod
    def get_all(cls, **options) -> list[Self]:
        cls._setup_model()
        options = cls._handle_options(options)
        objs = cls.sync_collection.find(options)

        if not objs:
            raise NoResult
        return [cls.from_dict(obj) for obj in objs]

    @classmethod
    def check_exists(cls, **options) -> bool:
        cls._setup_model()
        try:
            cls.get(**options)
            return True
        except NoResult:
            return False

    def add(self) -> None:
        if hasattr(self, "oid") and self.oid != EMPTY_OBJECTID:
            raise AlreadyExists
        dct = self.to_dict()
        del dct["_id"]
        result = self.sync_collection.insert_one(dct)
        self.oid = result.inserted_id

    def update(self) -> None:
        dct = self.to_dict()
        self.sync_collection.update_one({"_id": self.oid}, {"$set": dct})

    def delete(self) -> None:
        self.sync_collection.delete_one({"_id": self.oid})

    async def delete_async(self) -> None:
        await self.async_collection.delete_one({"_id": self.oid})

    async def update_async(self) -> None:
        dct = self.to_dict()
        await self.async_collection.update_one({"_id": self.oid}, {"$set": dct})

    async def add_async(self) -> None:
        if hasattr(self, "oid") and self.oid != EMPTY_OBJECTID:
            raise AlreadyExists
        dct = self.to_dict()
        del dct["_id"]
        result = await self.async_collection.insert_one(dct)
        self.oid = result.inserted_id

    @classmethod
    async def check_exists_async(cls, **options) -> bool:
        cls._setup_model()
        try:
            await cls.get_async(**options)
            return True
        except NoResult:
            return False

    @classmethod
    async def get_all_async(cls, **options) -> list[Self]:
        cls._setup_model()
        options = cls._handle_options(options)
        objs = cls.async_collection.find(options)
        objs = await objs.to_list(length=None)

        if not objs:
            raise NoResult
        return [cls.from_dict(obj) for obj in objs]

    @classmethod
    async def get_async(cls, **options) -> Self:
        cls._setup_model()
        options = cls._handle_options(options)
        obj = await cls.async_collection.find_one(options)

        if not obj:
            raise NoResult
        return cls.from_dict(obj)
