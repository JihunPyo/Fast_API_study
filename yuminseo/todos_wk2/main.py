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