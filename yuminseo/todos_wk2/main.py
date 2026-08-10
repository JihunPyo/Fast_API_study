from schema.response import TodoResponse #응답 모델 import
from schema.request import TodoCreateRequest, TodoUpdateRequest #생성, 수정 요청 모델 import
from fastapi import FastAPI, status, HTTPException

app = FastAPI() #FastAPI 애플리케이션 객체 생성

#할 일 데이터를 저장할 리스트 
todos = [   #임시 데이터 저장
    {"id": 1, "title": "FastAPI 공부하기", "is_done": False},
    {"id": 2, "title": "운동하기", "is_done": True},
    {"id": 3, "title": "책 읽기", "is_done": False}
]

#전체 할 일 조회
@app.get(   #GET API 정의
    "/todos", 
    response_model=list[TodoResponse], #응답 모델 지정 
    status_code=status.HTTP_200_OK
) #성공 시 반환할 상태 코드 지정
def get_todos_handler():
    return todos #할 일 데이터 리스트 반환

#단일 할 일 조회
@app.get(   #경로 변수를 사용하는 GET API 정의
    "/todos/{todo_id}", 
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def get_todo_handler(todo_id: int): 
    for todo in todos: #todos 리스트 순회 #단일 데이터 탐색
        if todo["id"] == todo_id:
            return todo 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="할 일 데이터를 찾을 수 없습니다.") #예외 처리 #데이터 없으면 404 에러 반환

#fastapi에서 엔드포인트 함수 이름 중복 XX
#따라서 전체 할 일 조회는 'get_todos_handler'로, 단일 할 일 조회는 'get_todo_handler'로 이름 지정

#할 일 생성
@app.post(
    "/todos", 
    response_model=TodoResponse, 
    status_code=status.HTTP_201_CREATED 
)
def create_todo_handler(body: TodoCreateRequest): #요청 본문을 매개변수로 받기
    new_todo = { #새 할 일 데이터 생성
        "id": len(todos) + 1, #id 값 생성
        "title": body.title, #요청 본문에서 title 가져오기
        "is_done": body.is_done #요청 본문에서 is_done 가져오기
    }
    todos.apend(new_todo) #리스트에 새 할 일 추가 후 응답 반환
    return new_todo

# 할 일 수정
@app.patch(
    "/todos/{todo_id}", 
    response_model=TodoResponse, 
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos: #수정 대상 데이터 탐색
        if todo["id"] == todo_id:
            if body.title is not None: #title 필드 조건부 수정
                todo["title"] = body.title 
            if body.is_done is not None: #is_done 필드 조건부 수정
                todo["is_done"] = body.is_done 
            return todo #수정된 데이터 반환
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="할 일 데이터를 찾을 수 없습니다.") #예외 처리

#할 일 삭제
@app.delete( #DELETE API 정의
    "/todos/{todo_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(todo_id: int):
    for todo in todos: #삭제 대상 데이터 탐색
        if todo["id"] == todo_id:
            todos.remove(todo) #리스트에서 데이터 삭제
            return #응답 본문 없이 함수 종료
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="할 일 데이터를 찾을 수 없습니다.") #예외 처리