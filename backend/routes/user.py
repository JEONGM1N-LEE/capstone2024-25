# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from backend.database.db import get_db
# from app.models.user import User
#
# router = APIRouter()
#
# @router.post("/users/")
# async def create_user(name: str, email: str, allergies: list, db: Session = Depends(get_db)):
#     new_user = User(name=name, email=email, allergies=allergies)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


