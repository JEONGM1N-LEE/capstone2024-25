from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.services.db_service import find_matching_allergies
from backend.database import get_db
from backend.models.allergy import AllergySynonyms  # 정확한 모델 참조

router = APIRouter()

@router.post("/check-allergy/")
async def check_allergy(text: str, db: Session = Depends(get_db)):
    """
    OCR 결과를 DB에서 검색하여 감지된 알러지 반환
    """
    matched_allergies = find_matching_allergies(db, text)
    return {"matched_allergies": matched_allergies}
