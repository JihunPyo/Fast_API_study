from pydantic import BaseModel

#할 일 생성 요청 모델
class TodoCreateRequest(BaseModel): #생성 요청 모델 이름 정의
    title: str #요청 본문 필드 구성 #할 일의 제목
    is_done: bool=False #할 일의 완료 여부

#할 일 수정 요청 모델
class TodoUpdateRequest(BaseModel): #수정 요청 모델 이름 정의
    title: str | None = None #선택 필드 설정 #요청 본문에서 생략된 필드는 None으로 전달
    is_done: bool | None = None