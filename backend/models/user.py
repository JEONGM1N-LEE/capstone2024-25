# 사용자 데이터를 저장하기 위한 데이터 모델을 정의
# from pydantic import BaseModel
#
# class User(BaseModel):
#     id: int
#     name: str
#     email: str

# from sqlalchemy import Column, Integer, String
# from app.database.db import Base
#
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     allergies = Column(String)  # 사용자별 알레르기 성분
