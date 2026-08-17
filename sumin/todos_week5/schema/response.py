from datetime import datetime
from pydantic import BaseModel

#할일 응답 모델
class TodoResponse(BaseModel): # BaseModel을 상속하여 pydantic 패키지로 관리할 수 있는 클래스로 만듦.
    id: int
    title: str
    is_done: bool

#회원가입 응답 모델
class UserSignUpResponse(BaseModel):
    id: int
    email: str
    created_at: datetime



