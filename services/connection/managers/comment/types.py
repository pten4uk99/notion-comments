import datetime

from pydantic import BaseModel

from services.connection.managers.types import DefaultResponseData, DataObjectType


class User(BaseModel):
    id: str


class Parent(BaseModel):
    block_id: str
    type: str


class Annotations(BaseModel):
    bold: bool
    code: bool
    color: str
    italic: bool
    strikethrough: bool
    underline: bool


class Text(BaseModel):
    content: str
    link: str = None


class RichTextElement(BaseModel):
    annotations: Annotations
    href: str = None
    plain_text: str
    text: Text
    type: str


class Comment(BaseModel):
    created_by: User
    created_time: datetime.datetime
    discussion_id: str
    id: str
    last_edited_time: datetime.datetime
    object: DataObjectType = DataObjectType.comment
    parent: Parent
    rich_text: list[RichTextElement]


class ResponseDataComment(DefaultResponseData):
    comment: dict
    has_more: bool
    # next_cursor = None
    object: DataObjectType = DataObjectType.list
    results: list[Comment]
    type: str
