# exam9.py

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
	name: str
	description: str | None = None
	price: float
	tax: float | None = None
	
app = FastAPI()
# {
#   "name":"alice",
#   "description": "이상한 나라의 앨리스",
#   "price" : 10000,
#   "tax": 0.1
# }

stored_item = None

@app.post("/items")
async def create_item(item: Item):
  global stored_item
  stored_item = item
  print(item)
  return item.name

@app.get('/items')
def get_item():
  return stored_item