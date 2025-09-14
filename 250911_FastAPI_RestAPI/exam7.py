from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/html1') #html file 로 응답하기
async def test1(request: Request):
  return templates.TemplateResponse('exam7-1.html', {'request':request})

