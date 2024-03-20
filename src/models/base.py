from time import time

from sqlalchemy import Column, Integer


class BaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(Integer, nullable=False, default=int(time()))
