from sqlalchemy import Column, String

from src.dependencies.database import Base
from src.models.base import BaseModel


class Link(Base, BaseModel):
    """Ресурс"""

    __tablename__ = "links"

    name = Column(String, unique=True, nullable=False)
    domain = Column(String, nullable=False)

    def __repr__(self):
        return f"<Ресурс {self.__dict__}>"
