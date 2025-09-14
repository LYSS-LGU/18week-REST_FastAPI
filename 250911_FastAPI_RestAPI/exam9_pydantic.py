from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
  id: int
  name: str
  email : Optional[str] = None
  active: bool = True  #필수, 값이 없으면 True 설정
  
#user = User(id=123, name='alice')
#print(user.id, user.email, user.active)

user_data_valid = {
  "id":'abc123',
  "name":'홍길동',
  "email":"hong"
}

try :
  user = User(**user_data_valid)
  print(user.id, type(user.id), user.email, user.active)
except Exception as e:
  print(f'***** 검증오류: {e}') 