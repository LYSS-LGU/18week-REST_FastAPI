from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/items/{id}', response_class=HTMLResponse) #html file 로 응답하기
async def read_item(request: Request, id:int):
  return templates.TemplateResponse('exam8_v.html', 
                                    {'request':request,
                                     'id':id,
                                     'nextid': 1 if id==10 else id+1,
                                     'img_name': f'images/{id}.jpg'
                                     })
