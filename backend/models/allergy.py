# PostgreSQL 테이블과 ORM 모델을 정확히 설정
# 알러지 정보 모델
from sqlalchemy import Column, Integer, String
from backend.database import Base

# 기존 DB 테이블과 연결
class AllergySynonyms(Base):
    __tablename__ = "allergy_synonyms"  # 기존 DB의 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    allergy_name = Column(String, index=True) # 알러지 성분명
    synonym = Column(String, index=True)      # 알러지 성분의 대체 이름
    description = Column(String, nullable=True)  # 🚀 설명 필드 추가
