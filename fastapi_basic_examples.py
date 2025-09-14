# C:\githome\18week-REST_FastAPI\fastapi_basic_examples.py
# FastAPI 기본 실습 예제 모음

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from enum import Enum
from typing import Optional
import uvicorn

# FastAPI 앱 생성
app = FastAPI(
    title="FastAPI 기본 실습",
    description="석이를 위한 FastAPI 학습 예제 모음",
    version="1.0.0"
)

# =============================================================================
# 1. 기본 라우트 예제들
# =============================================================================

@app.get("/")
async def root():
    """홈페이지 - 기본 딕셔너리 응답"""
    return {"message": "안녕하세요! FastAPI 실습에 오신 걸 환영합니다!"}

@app.get("/hello")
async def hello_world():
    """인사 메시지 반환"""
    return {"greeting": "안녕하세요, 석이!"}

@app.get("/items")
async def get_items():
    """리스트 형태의 응답"""
    return ["사과", "바나나", "오렌지", "포도", "딸기"]

@app.get("/html")
async def get_html():
    """HTML 직접 반환"""
    return "<h1>FastAPI로 만든 HTML 페이지</h1><p>HTML도 직접 반환 가능합니다!</p>"

@app.get("/count")
async def get_count():
    """숫자 반환 예제"""
    return 12345

# =============================================================================
# 2. 패스 매개변수 예제들
# =============================================================================

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    """사용자 ID로 사용자 정보 조회"""
    return {
        "user_id": user_id,
        "name": f"사용자_{user_id}",
        "status": "활성"
    }

@app.get("/product/{product_id}")
async def get_product(product_id: str):
    """상품 정보 조회"""
    return {
        "product_id": product_id,
        "name": f"상품_{product_id}",
        "price": 15000,
        "in_stock": True
    }

@app.get("/profile/{name}/{age}")
async def get_profile(name: str, age: int):
    """이름과 나이로 프로필 조회"""
    return {
        "name": name,
        "age": age,
        "message": f"{name}님은 {age}살입니다."
    }

# =============================================================================
# 3. 쿼리 매개변수 예제들
# =============================================================================

@app.get("/search")
async def search_items(q: str, limit: int = 10):
    """검색 기능 - 쿼리 매개변수 사용"""
    return {
        "query": q,
        "limit": limit,
        "results": [f"{q}_결과_{i}" for i in range(1, min(limit + 1, 6))]
    }

@app.get("/users")
async def get_users(skip: int = 0, limit: int = 100):
    """사용자 목록 페이지네이션"""
    users = [f"사용자_{i}" for i in range(skip + 1, skip + limit + 1)]
    return {
        "skip": skip,
        "limit": limit,
        "total": 1000,
        "users": users[:10]  # 처음 10개만 반환
    }

@app.get("/items/search")
async def search_items_advanced(
    q: str,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """고급 검색 기능"""
    filters = {}
    if category:
        filters["category"] = category
    if min_price:
        filters["min_price"] = min_price  
    if max_price:
        filters["max_price"] = max_price
    
    return {
        "query": q,
        "filters": filters,
        "results": f"'{q}' 검색 결과"
    }

# =============================================================================
# 4. Enum을 활용한 예제
# =============================================================================

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"
    sports = "sports"

@app.get("/category/{category_name}")
async def get_category_info(category_name: Category):
    """카테고리별 정보 조회"""
    category_info = {
        Category.electronics: "전자제품 카테고리입니다",
        Category.clothing: "의류 카테고리입니다", 
        Category.books: "도서 카테고리입니다",
        Category.food: "식품 카테고리입니다",
        Category.sports: "스포츠용품 카테고리입니다"
    }
    
    return {
        "category": category_name,
        "description": category_info.get(category_name, "알 수 없는 카테고리"),
        "available": True
    }

# =============================================================================
# 5. Path Converter 예제
# =============================================================================

@app.get("/files/{file_path:path}")
async def get_file_info(file_path: str):
    """파일 경로 정보 조회"""
    return {
        "file_path": file_path,
        "file_name": file_path.split("/")[-1] if "/" in file_path else file_path,
        "extension": file_path.split(".")[-1] if "." in file_path else "없음"
    }

# =============================================================================
# 6. Pydantic 모델을 활용한 요청 body 예제
# =============================================================================

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

@app.post("/users")
async def create_user(user: User):
    """새 사용자 생성"""
    return {
        "message": "사용자가 성공적으로 생성되었습니다",
        "user": user,
        "user_id": 12345
    }

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    """사용자 정보 수정"""
    return {
        "message": f"사용자 {user_id}가 성공적으로 수정되었습니다",
        "user_id": user_id,
        "updated_data": user
    }

# =============================================================================
# 7. HTTP 메소드 예제들
# =============================================================================

@app.post("/items")
async def create_item(name: str, price: float):
    """아이템 생성 (POST)"""
    return {
        "message": "아이템이 생성되었습니다",
        "item": {"name": name, "price": price, "id": 999}
    }

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, price: float):
    """아이템 전체 수정 (PUT)"""
    return {
        "message": f"아이템 {item_id}가 수정되었습니다",
        "item": {"id": item_id, "name": name, "price": price}
    }

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """아이템 삭제 (DELETE)"""
    return {
        "message": f"아이템 {item_id}가 삭제되었습니다",
        "deleted_id": item_id
    }

# =============================================================================
# 8. 에러 처리 예제
# =============================================================================

@app.get("/users/{user_id}/profile")
async def get_user_profile(user_id: int):
    """사용자 프로필 조회 - 에러 처리 예제"""
    if user_id < 1:
        return {"error": "사용자 ID는 1 이상이어야 합니다"}
    
    if user_id > 1000:
        return {"error": "존재하지 않는 사용자입니다"}
    
    return {
        "user_id": user_id,
        "name": f"사용자_{user_id}",
        "profile": "프로필 정보"
    }

# =============================================================================
# 서버 실행 부분
# =============================================================================

if __name__ == "__main__":
    print("🚀 FastAPI 서버를 시작합니다!")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🔄 서버 종료: Ctrl+C")
    
    uvicorn.run(
        "fastapi_basic_examples:app",
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )