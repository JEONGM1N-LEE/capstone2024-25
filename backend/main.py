from fastapi import FastAPI
from backend.routes.ocr import router as ocr_router
from backend.routes.allergy import router as allergy_router
from backend.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 데이터베이스 테이블 생성 (기존 DB가 있다면 실행하지 않아도 됨)
# Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(ocr_router)
# app.include_router(allergy_router)

@app.get("/")
async def root():
    return {"message": "🚀 FastAPI 서버가 성공적으로 실행되었습니다!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # SvelteKit이 실행되는 포트
    allow_methods=["*"],
    allow_headers=["*"],
)

