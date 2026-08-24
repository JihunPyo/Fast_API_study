#3장
from sentry_sdk import session
from unicodedata import normalize

from schema.response import TodoResponse #응답 모델 임포트
from schema.request import TodoCreateRequest, TodoUpdateRequest #생성, 수정 요청 모델 임포트
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

#할 일 저장
todos = [
    {"id":1, "title":"FastAPI 공부하기", "is_done":False}, #4장에서 데이터베이스 사용
    {"id":2, "title":"운동하기", "is_done":True},
    {"id":3, "title":"책 읽기", "is_done":False},
] #임시 데이터 저장

#전체 할 일 조회
@app.get( #GET API 정의 #"/todos" 경로로 데이터 조회 요청이 들어오면 get_todos_handler() 함수를 실행
    "/todos",
    response_model=list[TodoResponse], #TodoResponse 객체로 이루어진 리스트를 응답으로 반환
    status_code=status.HTTP_200_OK, #데이터 조회 요청이 성공했을 때 상태 코드 반환
)

def get_todos_handler():
    return todos

#단일 할 일 조회
@app.get( #경로 변수를 사용하는 GET API 정의
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)

def get_todo_handler(todo_id: int):
    for todo in todos: #단일 데이터 탐색 -> todos 리스트에서 저장된 각 할 일을 순회하며 각 항목의 id 값이 요청으로 전달된 todo_id와 일치하면 반환
        if todo["id"]==todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found")  # 요청은 정상적으로 처리되었지만 해당 데이터가 존재하지 않음

#할 일 생성
@app.post( #POST API 정의 #"/todos" 경로로 데이터 생성 요청이 들어오면 create_todo_handler() 함수를 실행
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)

def create_todo_handler(body: TodoCreateRequest): #요청 본문을 매개변수로 받기 (body를 매개변수로 받고, 타입을 TodoCreateRequest로 지정)
    new_todo={ #새 할 일 생성
        "id": len(todos) + 1, #id 값 생성 -> 현재 todos 항목이 3개라면, id는 4개 #+1하는 이유는 새로 추가할 일의 id를 자동으로 만들기 위함
        "title": body.title,
        "is_done": body.is_done,
    }
    todos.append(new_todo) #todos 리스트에 새 할 일 추가 후 응답 반환
    return new_todo

#할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)

def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos: #수정 대상 데이터 탐색
        if todo["id"]==todo_id:
            if body.title is not None: #title 필드 조건부 수정
                todo["title"] = body.title
            if body.is_done is not None: #is_done 필드 조건부 수정
                todo["is_done"] = body.is_done
            return todo #수정된 데이터 반환
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")  # 예외 처리


#할 일 삭제
@app.delete( #DELETE API 정의
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_todo_handler(todo_id: int):
    for todo in todos: #삭제 대상 데이터 탐색
        if todo["id"]==todo_id:
            todos.remove(todo) #id와 todo_id가 일치하는 항목을 찾으면 해당 항목을 todos 리스트에서 제거
            return #함수 종료
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

#4장

from fastapi import FastAPI, status, HTTPException
from database.db_connection import engine #데이터베이스 엔진 임포트
from database.orm import Base #ORM 기준 클래스 임포트
from models import Todo #ORM 모델 임포트

Base.metadata.create_all(bind=engine) #ORM 모델 정보를 바탕으로 테이블 생성 지시 #engine으로 연결된 데이터베이스에 테이블 생성

app = FastAPI()

from sqlalchemy import select #SELECT 쿼리 생성 도구 임포트
from database.db_connection import engine, SessionFactory #세션 팩토리 임포트

#전체 할 일 조회
@app.get(
    "/todos",
    response_model=list[TodoResponse], status_code=status.HTTP_200_OK,
)

def get_todos_handler():
    session = SessionFactory() #요청 단위 세션 생성 -> 요청마다 세션을 새로 만들도, 이 세션으로 DB 작업 수행
    try:
        stmt = select(Todo) #전체 조회 쿼리 객체 생성 -> Todo 모델에 대응되는 테이블을 조회하는 쿼리 객체 생성
        todos = session.execute(stmt).scalars().all() #쿼리 실행 및 결과 반환 -> 쿼리를 실행하고, 결과에서 Todo 객체를 모두 추출해 리스트로 변환
        return todos #조회된 Todos 반환
    finally:
        session.close() #세션 종료

#단일 할 일 조회
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)

def get_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id) #단일 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first() #쿼리 실행 및 단일 결과 선택
        if todo: #결과 반환
            return todo
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, #조회 실패 시 예외 처리
                            detail="Todo not found"
                            )
    finally:
        session.close()

#할 일 생성
@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)

def create_todo_handler(body: TodoCreateRequest):
    session = SessionFactory()
    try:
        todo = Todo( #ORM 모델 객체 생성
            title=body.title,
            is_done=body.is_done,
        )
        session.add(todo) #생성한 모델 객체를 세션에 등록
        session.commit() #DB에 저장
        return todo #할 일 생성 결과 반환
    finally:
        session.close()

#할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)

def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    session = SessionFactory()

    try:
        stmt = select(Todo).where(Todo.id == todo_id)  # 수정 대상 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first()  # 쿼리 실행 및 단일 결과 선택

        if todo:  # 조회 결과 확인
            if body.title is not None:  # 제목 수정
                todo.title = body.title

            if body.is_done is not None:  # 완료 여부 수정
                todo.is_done = body.is_done

            session.commit()  # 변경 사항 저장
            return todo  # 수정 결과 반환

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )  # 조회 실패 시 예외 처리

    finally:
        session.close()


#할 일 삭제
@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id) #삭제 대상 조회 쿼리 객체 생성
        todo = session.execute(stmt).scalars().first()  # 쿼리 실행 및 단일 결과 선택

        if todo:  # 조회 결과 확인
            session.delete(todo) #삭제 대상으로 지정
            session.commit() #변경 사항 저장
            return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )  # 조회 실패 시 예외 처리

    finally:
        session.close()