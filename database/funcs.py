from typing import Union, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, models_list, ModelType

from config import DB_URL


class DataBase:
    def __init__(self):
        self.Base = Base
        self.engine = create_engine(url=DB_URL)  # pyright: ignore
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()

    def create_all(self):
        self.Base.create_all(self.engine)

    def get_model(self, model: Union[ModelType, str]):  # -> ModelType:
        return getattr(models_list, str(model))

    def add(self, model: Union[ModelType, None], **kwargs):
        if not model:
            return

        new_data = model(**kwargs)
        data = self.session.query(model).filter_by(**kwargs).first()
        if data:
            return
        self.session.add(new_data)
        self.session.commit()

    def delete(self, model: Union[ModelType, None], id: int):
        if not model:
            return

        data = self.session.query(model).filter_by(id=id).first()
        if not data:
            return
        self.session.delete(data)
        self.session.commit()

    def update(self, model: Union[ModelType, None], id: int, new_data: Dict):
        if not model:
            return

        data = self.session.query(model).filter_by(id=id).first()
        if not data:
            return

        for key, value in new_data.items():
            setattr(data, key, value)
        self.session.commit()

    def get(self, model: Union[ModelType, None], **kwargs):
        if not model:
            return
        return self.session.query(model).filter_by(**kwargs).first()

    def get_all(self, model: Union[ModelType, None], **kwargs):
        if not model:
            return

        if kwargs:
            return [item for item in self.session.query(model).filter(**kwargs).all()]
        return [item for item in self.session.query(model).all()]

    def check_exist(self, model: Union[ModelType, None], id: int):
        if not model:
            return
        return self.session.query(model).filter_by(id=str(id)).first() is not None
