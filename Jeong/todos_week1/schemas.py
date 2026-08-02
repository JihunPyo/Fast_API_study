from pydantic import BaseModel

class Item(BaseModel):
    name:str
    price:int
    in_stock:bool = True