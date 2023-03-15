import datetime

from pydantic import BaseModel

from services.connection.managers.types import DefaultResponseData, DataObjectType


class ChildPage(BaseModel):
    title: str


class User(BaseModel):
    id: str


class Parent(BaseModel):
    type: str
    workspace: bool = None


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


class Paragraph(BaseModel):
    color: str
    rich_text: list[RichTextElement]


class ResponseDataBlock(DefaultResponseData):
    object = DataObjectType.block
    archived: bool
    child_page: ChildPage = None
    created_by: User
    created_time: datetime.datetime
    has_children: bool
    id: str
    last_edited_by: User
    last_edited_time: datetime.datetime
    parent: Parent
    paragraph: Paragraph = None
    type: str


class ResponseDataBlockChildren(DefaultResponseData):
    object = DataObjectType.list
    block: dict
    has_more: bool
    # next_cursor = None
    results: list[ResponseDataBlock]
    type: str
