# 데이터 베이스 연결 설정
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 기존에 만들어진 PostgreSQL 데이터베이스 연결
DATABASE_URL = "postgresql://postgres:Ecas5272%%@localhost/users_db"

# 데이터베이스 엔진 생성 (기존 DB에 연결)
engine = create_engine(DATABASE_URL)

# 세션 설정 (DB 연결 및 트랜잭션 관리)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델을 정의할 기본 클래스
Base = declarative_base()

# FastAPI에서 DB 세션을 가져오기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
