from fastapi import FastAPI
app = FastAPI()

#요청패스
@app.get('/')
async def root():  #핸들러
  return {'name':'내이름은 앨리스'}

@app.get('/test1')
async def root1():
  return {'name':'너는 누구니?'}  #딕셔너리 반환

@app.get('/test2')
async def root2():
  return ['앨리스','둘리','또치']

from fastapi.responses import HTMLResponse
@app.get('/test3')
async def root3():
  return HTMLResponse(content='<h1>안녕</h1>')

@app.get('/items/{item_id}')
async def read_item(item_id: int):
  return {'item_id입력값': item_id}