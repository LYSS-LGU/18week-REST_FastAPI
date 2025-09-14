from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Dooly"}, {"item_name": "Ddochi"}, {"item_name":
"Dauner"}, {"item_name": "Olaf"}]

@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10): 
	return fake_items_db[2 : 12]

@app.get("/items/{item_id}")
async def read_item_1(item_id: str, q: str | None = None): 
	if q:
		return {"item_id": item_id, "q": q}
	return {"item_id": item_id}