from pydantic import BaseModel

#할 일 응답 모델
class TodoResponse(BaseModel): #응답 모델 이름 정의
    id: int #응답 본문 필드 구성
    title: str
    is_done: bool