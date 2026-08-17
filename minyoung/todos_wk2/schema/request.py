from pydantic import BaseModel

#할 일 생성 요청 모델
class TodoCreateRequest(BaseModel): #생성 요청 모델 이름 정의
    title: str                      #요청 본문 필드 구성
    is_done: bool = False
    #id필드를 만들면 중복 id가 생성되어 기존 데이터와 충돌할 위험 있음. id는 서버가 생성하고, 클라이언트는 생성된 id를 응답으로 받아 활용

#할 일 수정 요청 모델
class TodoUpdateRequest(BaseModel): #수정 요청 모델 이름 정의
    title: str | None = None        #선택 필드 설정
    is_done: bool | None = None