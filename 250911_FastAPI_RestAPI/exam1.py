from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def root():
  return {'message':'안녕!!! fast api...'}

import uvicorn
if __name__ == "__main__":
  uvicorn.run('exam1:app', host='127.0.0.1', port=8002, reload=True)