# 🚀 FastAPI 초보자 실습 예제
# 이 파일은 단계별로 따라하면서 FastAPI를 배울 수 있는 완전한 예제입니다.

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# FastAPI 앱 생성
app = FastAPI(
    title="🎓 FastAPI 초보자 실습",
    description="단계별로 배우는 FastAPI",
    version="1.0.0"
)

# ============================================================================
# 📚 1단계: 기본 응답 타입들 (딕셔너리, 리스트, HTML, 숫자)
# ============================================================================

@app.get("/")
async def home():
    """메인 페이지 - 딕셔너리 반환"""
    return {
        "message": "🎉 FastAPI 초보자 실습에 오신 것을 환영합니다!",
        "guide": "각 엔드포인트를 차례대로 테스트해보세요",
        "docs": "http://localhost:8000/docs 에서 API 문서를 확인하세요"
    }

@app.get("/fruits")
async def get_fruits():
    """과일 목록 - 리스트 반환"""
    return ["🍎 사과", "🍌 바나나", "🍊 오렌지", "🍇 포도", "🥝 키위"]

@app.get("/greeting")
async def greeting_html():
    """HTML 인사말 - HTML 반환"""
    return HTMLResponse(content="""
    <html>
        <body style='font-family: Arial; text-align: center; margin: 50px;'>
            <h1 style='color: #4CAF50;'>🌟 안녕하세요!</h1>
            <p>FastAPI로 만든 첫 번째 HTML 페이지입니다.</p>
            <a href='/docs'>📖 API 문서 보기</a>
        </body>
    </html>
    """)

@app.get("/visitor-count")
async def visitor_count():
    """방문자 수 - 숫자 반환"""
    return 1234

# ============================================================================
# 📚 2단계: 패스 매개변수 (Path Parameters)
# ============================================================================

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """사용자 정보 조회 - 패스 매개변수"""
    return {
        "user_id": user_id,
        "name": f"사용자{user_id}",
        "status": "활성"
    }

@app.get("/products/{category}/{product_id}")
async def get_product(category: str, product_id: int):
    """상품 정보 조회 - 여러 패스 매개변수"""
    return {
        "category": category,
        "product_id": product_id,
        "name": f"{category} 상품 {product_id}번",
        "price": product_id * 1000
    }

@app.get("/files/{file_path:path}")
async def get_file_info(file_path: str):
    """파일 경로 처리 - Path Converter"""
    return {
        "file_path": file_path,
        "type": "파일" if "." in file_path else "폴더",
        "message": f"'{file_path}' 경로의 정보입니다"
    }

# ============================================================================
# 📚 3단계: 쿼리 매개변수 (Query Parameters)
# ============================================================================

@app.get("/search")
async def search_items(q: str = None, limit: int = 10, skip: int = 0):
    """검색 API - 쿼리 매개변수"""
    if not q:
        return {
            "message": "검색어를 입력하세요",
            "example": "/search?q=FastAPI&limit=5&skip=0"
        }
    
    # 가짜 검색 결과
    fake_results = [f"{q} 관련 결과 {i+1}" for i in range(limit)]
    
    return {
        "query": q,
        "results": fake_results,
        "total": len(fake_results),
        "skip": skip,
        "limit": limit
    }

@app.get("/weather")
async def get_weather(city: str = "서울", units: str = "celsius"):
    """날씨 API - 기본값이 있는 쿼리 매개변수"""
    weather_data = {
        "서울": {"temp": 23, "condition": "맑음"},
        "부산": {"temp": 26, "condition": "흐림"},
        "제주": {"temp": 25, "condition": "비"}
    }
    
    city_weather = weather_data.get(city, {"temp": 20, "condition": "알 수 없음"})
    
    return {
        "city": city,
        "temperature": city_weather["temp"],
        "condition": city_weather["condition"],
        "units": units
    }

# ============================================================================
# 📚 4단계: Pydantic 모델을 사용한 데이터 검증
# ============================================================================

class Student(BaseModel):
    """학생 정보 모델"""
    name: str
    age: int
    grade: str
    subjects: Optional[List[str]] = []
    is_active: bool = True

class StudentResponse(BaseModel):
    """학생 응답 모델"""
    id: int
    student: Student
    message: str

# 가짜 데이터베이스
students_db = []
student_id_counter = 1

@app.post("/students", response_model=StudentResponse)
async def create_student(student: Student):
    """학생 등록 - POST 요청과 Pydantic 모델"""
    global student_id_counter
    
    # 데이터 검증 (나이 체크)
    if student.age < 5 or student.age > 100:
        raise HTTPException(status_code=400, detail="나이는 5세에서 100세 사이여야 합니다")
    
    # 학생 저장
    student_data = {
        "id": student_id_counter,
        "student": student,
        "created_at": "2024-01-01"
    }
    students_db.append(student_data)
    
    response = StudentResponse(
        id=student_id_counter,
        student=student,
        message=f"{student.name} 학생이 성공적으로 등록되었습니다!"
    )
    
    student_id_counter += 1
    return response

@app.get("/students")
async def get_all_students():
    """모든 학생 조회"""
    return {
        "total": len(students_db),
        "students": students_db
    }

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    """특정 학생 조회"""
    for student_data in students_db:
        if student_data["id"] == student_id:
            return student_data
    
    raise HTTPException(status_code=404, detail="학생을 찾을 수 없습니다")

# ============================================================================
# 📚 5단계: HTML 폼과 템플릿 (간단한 웹 페이지)
# ============================================================================

@app.get("/register-form", response_class=HTMLResponse)
async def show_register_form():
    """학생 등록 폼 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>학생 등록</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .result { margin-top: 20px; padding: 10px; background-color: #f0f0f0; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🎓 학생 등록 시스템</h1>
        
        <form id="studentForm">
            <div class="form-group">
                <label for="name">이름:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="age">나이:</label>
                <input type="number" id="age" name="age" min="5" max="100" required>
            </div>
            
            <div class="form-group">
                <label for="grade">학년:</label>
                <select id="grade" name="grade" required>
                    <option value="">선택하세요</option>
                    <option value="초등학교">초등학교</option>
                    <option value="중학교">중학교</option>
                    <option value="고등학교">고등학교</option>
                    <option value="대학교">대학교</option>
                </select>
            </div>
            
            <button type="submit">등록하기</button>
        </form>
        
        <div id="result" class="result" style="display: none;"></div>
        
        <hr>
        <p><a href="/docs">📖 API 문서 보기</a> | <a href="/students">👥 등록된 학생 보기</a></p>
        
        <script>
            document.getElementById('studentForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const studentData = {
                    name: formData.get('name'),
                    age: parseInt(formData.get('age')),
                    grade: formData.get('grade'),
                    subjects: [],
                    is_active: true
                };
                
                try {
                    const response = await fetch('/students', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(studentData)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('result').innerHTML = 
                            '<h3 style="color: green;">✅ ' + result.message + '</h3>' +
                            '<p>학생 ID: ' + result.id + '</p>';
                        document.getElementById('result').style.display = 'block';
                        e.target.reset();
                    } else {
                        document.getElementById('result').innerHTML = 
                            '<h3 style="color: red;">❌ 오류: ' + result.detail + '</h3>';
                        document.getElementById('result').style.display = 'block';
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 
                        '<h3 style="color: red;">❌ 네트워크 오류가 발생했습니다.</h3>';
                    document.getElementById('result').style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ============================================================================
# 📚 6단계: 에러 처리와 상태 코드
# ============================================================================

@app.get("/divide/{a}/{b}")
async def divide_numbers(a: float, b: float):
    """나눗셈 계산 - 에러 처리 예제"""
    if b == 0:
        raise HTTPException(
            status_code=400, 
            detail="0으로 나눌 수 없습니다!"
        )
    
    result = a / b
    return {
        "a": a,
        "b": b,
        "result": result,
        "message": f"{a} ÷ {b} = {result}"
    }

@app.get("/status-demo/{code}")
async def status_code_demo(code: int):
    """HTTP 상태 코드 데모"""
    if code == 200:
        return {"message": "성공!", "status": "OK"}
    elif code == 404:
        raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다")
    elif code == 500:
        raise HTTPException(status_code=500, detail="서버 내부 오류")
    else:
        return {"message": f"상태 코드 {code}를 요청하셨습니다", "info": "200, 404, 500을 시도해보세요"}

# ============================================================================
# 📚 7단계: 실용적인 미니 API들
# ============================================================================

@app.get("/random-quote")
async def get_random_quote():
    """랜덤 명언 API"""
    quotes = [
        {"text": "코딩은 예술이다", "author": "개발자"},
        {"text": "버그는 기능이다", "author": "시니어 개발자"},
        {"text": "문서화가 가장 어렵다", "author": "모든 개발자"},
        {"text": "FastAPI는 정말 빠르다", "author": "Python 개발자"}
    ]
    import random
    return random.choice(quotes)

@app.get("/calculator")
async def calculator(a: float, b: float, operation: str = "add"):
    """간단한 계산기 API"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Cannot divide by zero"
    }
    
    if operation not in operations:
        raise HTTPException(status_code=400, detail="지원하지 않는 연산입니다. add, subtract, multiply, divide 중 선택하세요.")
    
    return {
        "a": a,
        "b": b,
        "operation": operation,
        "result": operations[operation]
    }

# ============================================================================
# 📚 8단계: 도움말과 가이드
# ============================================================================

@app.get("/help")
async def get_help():
    """API 사용 가이드"""
    return {
        "🎯 초보자 가이드": {
            "1단계": "기본 엔드포인트들을 테스트해보세요 (/, /fruits, /greeting)",
            "2단계": "패스 매개변수를 사용해보세요 (/users/123, /products/electronics/456)",
            "3단계": "쿼리 매개변수를 사용해보세요 (/search?q=FastAPI&limit=5)",
            "4단계": "학생 등록 API를 사용해보세요 (POST /students)",
            "5단계": "웹 폼을 사용해보세요 (/register-form)",
            "6단계": "에러 처리를 확인해보세요 (/divide/10/0)",
            "7단계": "실용적인 API들을 사용해보세요 (/random-quote, /calculator)"
        },
        "📖 문서": "http://localhost:8000/docs",
        "🎮 테스트 페이지": "http://localhost:8000/register-form",
        "💡 팁": [
            "/docs 페이지에서 모든 API를 테스트할 수 있습니다",
            "각 API의 응답을 확인하여 FastAPI의 기능을 이해하세요",
            "에러가 발생하면 상태 코드와 메시지를 확인하세요",
            "Pydantic 모델을 사용하면 자동으로 데이터 검증이 됩니다"
        ]
    }

# ============================================================================
# 🚀 서버 실행 코드
# ============================================================================

if __name__ == "__main__":
    print("🚀 FastAPI 초보자 실습 서버를 시작합니다!")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🎮 테스트 페이지: http://localhost:8000/register-form")
    print("❓ 도움말: http://localhost:8000/help")
    print("⭐ 메인 페이지: http://localhost:8000/")
    print("\n🛑 서버를 중지하려면 Ctrl+C를 누르세요")
    
    uvicorn.run(
        "초보자_실습예제:app",  # 파일명:앱객체명
        host="127.0.0.1",
        port=8000,
        reload=True  # 코드 변경 시 자동 재시작
    )

# ============================================================================
# 📝 실습 가이드
# ============================================================================
"""
🎓 실습 방법:

1. 이 파일을 실행하세요:
   python 초보자_실습예제.py

2. 브라우저에서 다음 주소들을 차례대로 방문해보세요:
   - http://localhost:8000/ (메인 페이지)
   - http://localhost:8000/docs (API 문서)
   - http://localhost:8000/help (도움말)
   - http://localhost:8000/register-form (웹 폼 테스트)

3. API 문서(/docs)에서 각 엔드포인트를 테스트해보세요:
   - GET 요청들은 바로 실행 가능
   - POST 요청은 JSON 데이터 입력 필요

4. 다양한 매개변수 조합을 시도해보세요:
   - /users/123
   - /search?q=FastAPI&limit=3
   - /calculator?a=10&b=5&operation=multiply

5. 에러 상황도 테스트해보세요:
   - /divide/10/0 (0으로 나누기)
   - /students/999 (존재하지 않는 학생)

🎯 학습 목표:
- FastAPI의 기본 구조 이해
- 다양한 HTTP 메소드 사용법
- 패스/쿼리 매개변수 활용
- Pydantic을 통한 데이터 검증
- 에러 처리 방법
- HTML 응답과 웹 폼 처리

💡 추가 실습:
- 코드를 수정해보고 변화 확인
- 새로운 엔드포인트 추가
- 다른 Pydantic 모델 생성
- 더 복잡한 비즈니스 로직 구현
"""
