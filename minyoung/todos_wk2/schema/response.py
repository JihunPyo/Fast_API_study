from pydantic import BaseModel

#할 일 응답 모델
class TodoResponse(BaseModel): #응답 모델 이름 정의
    id: int  #할일 데이터 고유 id    #응답 본문 필드 구성
    title: str #할일 데이터 제목
    is_done: bool #할일 완료 여부