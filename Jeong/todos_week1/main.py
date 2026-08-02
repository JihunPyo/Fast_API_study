from fastapi import FastAPI,status
from schemas import Item

app=FastAPI()

@app.get("/")
def get_root():
    return{"say":"Welcome"}

@app.get("/login")
def login_handler(name:str): # 쿼리 파라미터로 name을 받음
    return{"message":f"Hello {name}, you are logged in!"}

@app.get("/users/{user_id}")
def get_user(user_id:int): # 경로 파라미터로 user_id를 받음
    return{"user_id":user_id,"message":f"사용자 {user_id} 정보 조회"}

@app.post("/items",response_model=Item,status_code=status.HTTP_201_CREATED)
def create_item_handler(item:Item):
    return item
        #{"message":f"Item {item.name}이 추가되었습니다,",
        #          "item":item}

@app.put("/items/{item_id}")
def update_item_handler(item_id:int,assignee:str,item:Item):
    return{
        "item_id":item_id,
        "assignee":assignee,
        "item":item
    }