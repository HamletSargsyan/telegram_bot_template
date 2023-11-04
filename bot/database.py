from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Union, List

from config import DB_URL

import threading

db_lock = threading.Lock()

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

