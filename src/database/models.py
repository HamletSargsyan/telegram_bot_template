from dataclasses import dataclass, field
from datetime import datetime

from database.base import BaseModel
from helpers.datetime_utils import utcnow


@dataclass
class UserModel(BaseModel):
    __settings__ = {
        "collection_name": "users",
    }
    id: int
    name: str
    registered_at: datetime = field(default_factory=utcnow)
