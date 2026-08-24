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
