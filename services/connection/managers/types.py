from enum import Enum

from pydantic import BaseModel


class DataObjectType(str, Enum):
    error = 'error'
    page = 'page'
    block = 'block'
    list = 'list'
    comment = 'comment'
    user = 'user'


class PageParentType(str, Enum):
    workspace = 'workspace'


class DefaultResponseData(BaseModel):
    object: DataObjectType


class ResponseDataError(DefaultResponseData):
    status: int
    code: str
    message: str


