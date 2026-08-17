from pydantic import BaseModel

class TodoCreateRequest(BaseModel):
    title: str
    is_done: bool=False #선택필드

class TodoUpdateRequest(BaseModel):
    title: str | None = None
    is_done: bool | None = None # 이 필드는 안거드릴 수 있다의 의미
    

