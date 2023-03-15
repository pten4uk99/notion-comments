import datetime

from pydantic import BaseModel

from services.connection.managers.types import PageParentType, DefaultResponseData


class PageUser(BaseModel):
    id: str


class PageParent(BaseModel):
    type: PageParentType
    workspace: bool


class PagePropertiesTitleElementText(BaseModel):
    content: str
    link: str = None


class PagePropertiesTitleElementAnnotations(BaseModel):
    bold: bool
    italic: bool
    strikethrough: bool
    underline: bool
    code: bool
    color: str


class PagePropertiesTitleElement(BaseModel):
    type: str
    text: PagePropertiesTitleElementText
    annotations: PagePropertiesTitleElementAnnotations
    plain_text: str
    href: str = None


class PagePropertiesTitle(BaseModel):
    id: str
    type: str
    title: list[PagePropertiesTitleElement]


class PageProperties(BaseModel):
    title: PagePropertiesTitle


class ResponseDataPage(DefaultResponseData):
    id: str
    created_time: datetime.datetime
    last_edited_time: datetime.datetime
    created_by: PageUser
    last_edited_by: PageUser
    # cover = None
    # icon = None
    parent: PageParent
    archived: bool
    properties: PageProperties
    url: str
