from pydantic import BaseModel

from services.connection.managers.types import DataObjectType


class Person(BaseModel):
    email: str


class User(BaseModel):
    avatar_url: str = None
    id: str
    name: str
    object: DataObjectType
    person: Person
    type: str
