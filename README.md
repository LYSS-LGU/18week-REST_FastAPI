# ⚡ FastAPI 완전정리 가이드 (초보자용)

## 📋 목차

1. [REST API란?](#1-rest-api란)
2. [FastAPI 환경설정](#2-fastapi-환경설정)
3. [FastAPI 소개와 특징](#3-fastapi-소개와-특징)
4. [FastAPI 개발 시작하기](#4-fastapi-개발-시작하기)
5. [요청 패스 정의](#5-요청-패스-정의)
6. [실습 예제 모음](#6-실습-예제-모음)

---

## 1. REST API란?

### 🌐 REST의 기본 개념

- **REST**: REpresentational State Transfer의 약어
- **핵심 원리**: 하나의 URI는 하나의 고유한 리소스를 대표
- **목적**: 웹의 장점을 최대한 활용할 수 있는 아키텍처

### 🔧 REST API 설계 기본 규칙

#### 1️⃣ URI는 자원을 표현

```
❌ 잘못된 예: GET /members/delete/1
✅ 올바른 예: DELETE /members/1
```

#### 2️⃣ HTTP 메소드로 행위 표현

| 메소드 | 용도      | 예시              |
| ------ | --------- | ----------------- |
| GET    | 조회      | `GET /users/1`    |
| POST   | 생성      | `POST /users`     |
| PUT    | 전체 수정 | `PUT /users/1`    |
| PATCH  | 부분 수정 | `PATCH /users/1`  |
| DELETE | 삭제      | `DELETE /users/1` |

### 📡 HTTP 상태 코드

| 코드 | 의미         | 사용 예시                 |
| ---- | ------------ | ------------------------- |
| 200  | 성공         | GET 요청 성공             |
| 201  | 생성됨       | POST 요청으로 리소스 생성 |
| 400  | 잘못된 요청  | 클라이언트 오류           |
| 404  | 찾을 수 없음 | 존재하지 않는 리소스      |
| 500  | 서버 오류    | 서버 내부 오류            |

---

## 2. FastAPI 환경설정

### 🐍 Conda 가상환경 생성

```bash
# 1. 가상환경 생성
conda create -n fastapi_env python=3.10 -c conda-forge -y

# 2. 가상환경 활성화
conda activate fastapi_env

# 3. FastAPI 및 필수 라이브러리 설치
conda install -c conda-forge fastapi uvicorn pydantic -y
```

### 📦 필수 라이브러리 설명

- **FastAPI**: 웹 프레임워크
- **Uvicorn**: ASGI 서버 (FastAPI 실행용)
- **Pydantic**: 데이터 검증 라이브러리

---

## 3. FastAPI 소개와 특징

### ⚡ 주요 특징

1. **높은 성능**: Node.js, Go와 대등한 성능
2. **비동기 처리**: ASGI 기반으로 빠른 처리
3. **자동 문서화**: Swagger UI 자동 생성
4. **데이터 검증**: Pydantic을 통한 자동 검증
5. **타입 힌트**: Python 3.8+ 타입 힌트 완벽 지원

### 🚀 FastAPI의 장점

- **쉬운 학습**: Flask와 비슷한 구조
- **마이크로서비스**: 작은 서비스 개발에 최적
- **ML 서비스**: 머신러닝 API 개발에 편리
- **자동 문서**: 코드 작성만으로 API 문서 자동 생성

### 🎯 언제 사용할까?

- ✅ 작은 규모의 웹 애플리케이션
- ✅ API 개발 중심 프로젝트
- ✅ 마이크로서비스 아키텍처
- ✅ ML 모델 서빙
- ✅ 빠른 프로토타이핑

---

## 4. FastAPI 개발 시작하기

### ⚡ 기본 앱 구조

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}
```

### 💻 서버 실행 방법

#### 방법 1: CLI로 실행

```bash
uvicorn main:app --reload
```

#### 방법 2: Python 코드로 실행

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

### 🌐 접속 URL

- **메인 페이지**: http://localhost:8000/
- **API 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc

---

## 5. 요청 패스 정의

### 🔄 기본 응답 타입들

#### 1️⃣ 딕셔너리 반환 (가장 일반적)

```python
@app.get("/user")
async def get_user():
    return {"name": "홍길동", "age": 25}
```

#### 2️⃣ 리스트 반환

```python
@app.get("/fruits")
async def get_fruits():
    return ["사과", "바나나", "오렌지"]
```

#### 3️⃣ HTML 반환

```python
@app.get("/hello")
async def hello_html():
    return "<h1>안녕하세요!</h1>"
```

#### 4️⃣ 숫자 반환

```python
@app.get("/count")
async def get_count():
    return 1000
```

### 🛣️ 패스 매개변수 (Path Parameters)

```python
# 기본 패스 매개변수
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# 여러 패스 매개변수
@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}
```

### 🔍 쿼리 매개변수 (Query Parameters)

```python
@app.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 선택적 매개변수
@app.get("/search")
async def search_items(q: str = None):
    if q:
        return {"query": q}
    return {"message": "검색어를 입력하세요"}
```

### 📂 Path Converter (파일 경로 처리)

```python
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path}
```

---

## 6. 실습 예제 모음

### 💡 예제 1: 기본 API

```python
from fastapi import FastAPI

app = FastAPI(title="내 첫 번째 FastAPI")

@app.get("/")
async def home():
    return {"message": "FastAPI 학습 중입니다!"}

@app.get("/about")
async def about():
    return {"name": "홍길동", "job": "개발자"}
```

### 👥 예제 2: 사용자 관리 API

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# 가짜 데이터베이스
users_db = [
    {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    {"id": 2, "name": "김철수", "email": "kim@example.com"},
]

@app.get("/users")
async def get_users():
    return users_db

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    return {"error": "사용자를 찾을 수 없습니다"}
```

### 🔒 예제 3: Pydantic 모델 사용

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

@app.post("/users")
async def create_user(user: User):
    return {"message": f"{user.name}님이 등록되었습니다!", "user": user}
```

### 🌐 예제 4: HTML 템플릿 사용

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/page/{name}", response_class=HTMLResponse)
async def get_page(request: Request, name: str):
    return templates.TemplateResponse("user.html", {
        "request": request,
        "name": name
    })
```

---

## 📊 학습 포인트 요약

### ✅ 꼭 기억할 것들

1. **REST 원칙**: URI는 자원, HTTP 메소드는 행위
2. **FastAPI 특징**: 빠르고, 쉽고, 자동 문서화
3. **패스 vs 쿼리**: 필수는 패스, 선택은 쿼리
4. **Pydantic**: 데이터 검증의 핵심
5. **비동기**: `async def`로 성능 향상

### 🔧 개발 팁

- `--reload` 옵션으로 개발 시 자동 재시작
- `/docs`에서 API 테스트 가능
- 타입 힌트 사용으로 자동 검증
- 에러 처리는 HTTPException 사용

### 📚 다음 단계

1. 데이터베이스 연동 (SQLAlchemy)
2. 인증/권한 처리 (JWT)
3. 파일 업로드/다운로드
4. 백그라운드 작업 (Celery)
5. 테스팅 (pytest)

---

## 🔗 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/ko/)
- [FastAPI GitHub](https://github.com/fastapi/fastapi)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Uvicorn 문서](https://www.uvicorn.org/)

---

## 📁 추가 학습 자료

이 저장소에는 다음과 같은 추가 학습 자료들이 포함되어 있습니다:

### 🎯 실습 파일들

- `초보자_실습예제.py`: 혼자서도 실습할 수 있는 완전한 FastAPI 예제
- `FastAPI_학습로드맵.md`: 초보자부터 실무자까지의 단계별 학습 계획

### 🚀 빠른 시작

1. 가상환경 설정 후 `초보자_실습예제.py` 실행
2. 브라우저에서 http://localhost:8000/docs 접속
3. 각 API 엔드포인트 테스트해보기

_이 가이드는 FastAPI 학습을 위한 완전한 참고 자료입니다. 단계별로 따라하면서 실습해보세요! 🚀_
