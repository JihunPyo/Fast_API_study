from pydantic import BaseModel, ConfigDict

class BlogRequest(BaseModel):
    title: str
    content: str
    model_config = ConfigDict(from_attributes=True)


class BlogUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    model_config = ConfigDict(from_attributes=True)