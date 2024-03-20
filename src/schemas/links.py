from typing import List

from pydantic import BaseModel


class EntryBase(BaseModel):
    links: List[str]


class Entry(EntryBase):
    class Config:
        orm_mode = True
