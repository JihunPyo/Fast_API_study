from schema.response import BlogResponse #응답 모델 불러오기
from schema.request import BlogCreateRequest, BlogUpdateRequest #생성 요청 모델 불러오기
from fastapi import FastAPI, status, HTTPException

app = FastAPI()
#할 일 저장
blog = [
    {"id": 1, "title": "공부 브이로그", "content": "수학 공부"},
    {"id": 2, "title": "운동 브이로그", "content": "하체 운동"},
    {"id": 3, "title": "독후감", "content": "우중괴담"},
]
#전체 할 일 조회
@app.get(
    "/blog",
    response_model=list[BlogResponse], #TOdoResponse 객체로 이루어진 리스트 반환
    status_code=status.HTTP_200_OK #데이터 조회 요청이 성고했을 때의 상태 코드 반환
)
#/todos 경로로 데이터 조회 요청시 아래 함수를 실행
def get_todos_handler():
    return blog

@app.get(
    "/todos/{todo_id}", #{todo_id}는 경로 변수로, 경로변수에 정수 값을 넣으면 todo_id에 저장되어 아래 함수의 매개변수로 전달
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK #데이터 조회 요청이 성고했을 때의 상태 코드 반환
)
def get_todo_handler(todo_id: int): #todo_id를 int로 정의하여 FastAPI는 전달된 값이 정수인지 자동 검증
    for todo in blog:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

@app.post(
    "/todos",
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(body: BlogCreateRequest): #요청 본문을 body 매개변수로 받고 타입을 TodoCreateRequest로 지정
    new_todo = { #새 할일 데이터 생성하고 new_todo에 저장
        "id": len(blog) +1,
        "title": body.title,
        "is_done": body.is_done,
    }
    blog.append(new_todo) #new_todo를 todos 리스트에 추가
    return new_todo #생성된 데이터를 응답으로 반환

@app.patch(
    "/todos/{todo_id}",
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: BlogUpdateRequest):
    for todo in blog:
        if todo["id"] == todo_id:
            if body.title is not None:
                todo["title"] = body.title
            if body.is_done is not None:
                todo["is_done"] = body.is_done
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(todo_id: int):
    for todo in blog:
        if todo["id"] == todo_id:
            blog.remove(todo)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")