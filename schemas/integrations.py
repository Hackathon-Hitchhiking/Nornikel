import enum

from pydantic import BaseModel


class ResponseType(enum.Enum):
    PDF = "pdf"


class PageResponse(BaseModel):
    title: str
    content: bytes | str
    type: ResponseType  # the type of the returning document
