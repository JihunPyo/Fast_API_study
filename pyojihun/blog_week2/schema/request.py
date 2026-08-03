from pydantic import BaseModel

class BlogRequest(BaseModel):
    title: str
    content: str

class BlogUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None