from pydantic import BaseModel

class TodoResponse(BaseModel): #API 응답에 사용할 모델(클라이언트에 반환되는 데이터 구조 정의) 만들기
    id: int
    title: str
    is_done: bool