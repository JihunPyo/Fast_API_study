from fastapi import FastAPI, status
from pydantic import BaseModel

app: FastAPI = FastAPI() # Fastapi로의 메인 엔트리포인트

@app.get("/")
def root_handler():
    return {"message": "Hello FastAPI!"}



@app.get("/login")
def login_handler():
    return {"message": "로그인 페이지에 오신 것을 환영합니다."}

@app.get("/users/{user_id}")
def read_user(user_id: int): # 타입 힌트 지정. 만약 타입 힌트를 안준다면 FastAPI는 user_id를 str로 인식함!!
    return {"user_id": user_id}

#쿼리 파라미터 사용 엔드포인트 작성
@app.get("/items")
def read_items_handler(max_price: int | None = None): # 쿼리 파라미터는 기본값을 지정할 수 있음. 기본값이 없으면 필수 파라미터로 인식됨
    return {"max_price": max_price}
#None=> Optional[int]과 동일. 즉, max_price는 int 또는 None이 될 수 있음.

class Item(BaseModel): # Pydantic 모델 정의. FastAPI는 Pydantic 모델을 사용하여 요청 바디를 검증하고 직렬화함.
    name: str
    price: int
    in_stock: bool = True

#새 아이템 생성 엔드포인트 작성
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED) # 요청 바디를 Pydantic 모델로 받음. type hinting을 통해 FastAPI는 요청 바디를 자동으로 파싱하고 검증함.
def create_item_handler(item: Item): # 요청 바디를 Pydantic 모델로 받음. type hinting을 통해 FastAPI는 요청 바디를 자동으로 파싱하고 검증함.
    return item

@app.put("/items/{item_id}") #put 메서드로 아이템 업데이트 엔드포인트 작성
def update_item_handler(item_id: int, assignee: str, item: Item): # 요청 바디를 Pydantic 모델로 받음. type hinting을 통해 FastAPI는 요청 바디를 자동으로 파싱하고 검증함.
    return {"item_id": item_id,
            "assignee": assignee,
            "item": item}