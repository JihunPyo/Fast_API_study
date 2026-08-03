from pydantic import BaseModel

class TodoCreateRequest(BaseModel): #생성 요청 본문 검증 모델 정의
    title: str #요청 본문 필드
    is_done: bool = False

class TodoUpdateRequest(BaseModel): #수정 요청 모델 이름 정의
    title: str | None = None #선택 필드 설정 - 모든 필드를 선택 필드로 설정하여 요청 본문에서 생략된 필드는 None으로 전달, 서버는 해당 필드를 수정하지 않음
    is_done: bool |None = None