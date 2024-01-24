from typing import Union

from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import MetaData

Base: MetaData = declarative_base()

# pyright: reportGeneralTypeIssues=false

# EDIT
models_list = []
ModelType = Union[Base, Base]
models_dict = {}
