from pydantic import BaseModel


class SearchByTextRequest(BaseModel):
    text: str
