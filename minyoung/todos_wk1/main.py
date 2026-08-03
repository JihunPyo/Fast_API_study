from fastapi import FastAPI, status

app = FastAPI() #FastAPI 애플리케이션 객체 생성

#서버 실행
@app.get("/") #루트 경로에 GET 요청이 들어오면 root_handler 함수를 실행
def root_handler():
    return {"message": "Hello World!"} #Python dict 객체지만 FastAPI가 JSON으로 직렬화해서 응답 반환 (즉, Python 데이터를 JSON 텍스트로 바꿔서 HTTP 응답으로 전달)

#경로 사용
@app.get("/login") #GET 요청과 경로 매핑 설정
def login_handler():
    return{"message": "로그인 페이지에 오신 것을 환영합니다."} #요청을 처리하는 함수 정의

#경로 변수 사용
@app.get("/users/{user_id}") #동적 경로! 경로 변수 user_id를 사용하여 요청 처리
def get_user_handler(user_id: int): 
    return {"user_id": user_id, "message": f"사용자 {user_id} 정보 조회"} 

#쿼리 파라미터 사용
@app.get("/items")
def read_items_handler(max_price: int | None = None): 
    return{"max_price": max_price}

#아이템 모델 정의
class Item(BaseModel): #요청 본문 검증을 위한 Item 모델 정의
    name: str
    price: int
    in_stock: bool = True

#새 아이템 등록
@app.post("/items") #POST 요청과 경로 매핑 설정
def create_item_handler(item: Item): #요청 본문데이터를 Item 객체로 변환
    return {"message": f"아이템 {item.name}이(가) 추가되었습니다.", "item": item}

#경로 변수, 쿼리 파라미터, 요청 본문 혼합 사용
@app.put("/items/{item_id}")
def update_item_handler(item_id: int, assignee: str, item: Item):
    return {
        "item_id": item_id, 
        "assignee": assignee, #담당자 또는 작업자
        "item": item
    }

#새 아이템 등록
@app.post("/items", 
          response_model=Item, #응답 데이터를 Item 모델로 지정
          status_code=status.HTTP_201_CREATED) #성공 시 반환할 상태 코드 지정
def create_item_handler(item: Item):
    return item #Item 객체를 그대로 반환


#주문 응답 모델
class OrderResponse(BaseModel):
  order_id: int, 
  pickup: bool | None = None
  
#단일 주문 조회
@app.get("/orders/{orser_id}", reponse_model=OrderResponse)
def get_order_handler(order_id: int, pickup:bool | None = None):
  return {
      "order_id": order_id,
      "pickup": pickup
}