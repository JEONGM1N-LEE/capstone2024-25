# PostgreSQL 데이터베이스에서 알러지 성분 검색
import re
from sqlalchemy.orm import Session
from backend.models.allergy import AllergySynonyms


def _normalize(text: str) -> str:
    return re.sub(r"[\s,./()\[\]:：·•\-_+]", "", (text or "")).lower()


def _term_in_text(normalized: str, term: str) -> bool:
    key = (term or "").strip().lower()
    if not key or key not in normalized:
        return False
    # "밀크" 안의 "밀"은 밀 알레르기로 보지 않음
    if key == "밀":
        masked = normalized.replace("밀크", "").replace("milk", "")
        return "밀" in masked
    return True


def find_matching_allergies(db: Session, text: str):
    """OCR 결과에서 알러지 성분과 일치하는 항목 찾기"""
    if (text or "").startswith("🚨"):
        return text

    normalized = _normalize(text)
    if not normalized:
        return "🚨 OCR 오류: 이미지에서 글자를 읽지 못했습니다."

    matched_allergies = set()
    allergy_descriptions = {}

    allergies = db.query(AllergySynonyms).all()

    for allergy in allergies:
        synonyms_list = [s.strip() for s in (allergy.synonym or "").split(",") if s.strip()]
        all_names = [allergy.allergy_name] + synonyms_list
        if any(_term_in_text(normalized, name) for name in all_names):
            matched_allergies.add(allergy.allergy_name)
            allergy_descriptions[allergy.allergy_name] = getattr(allergy, "description", None) or "📌 설명 없음"

    if matched_allergies:
        allergy_list = [
            f"{allergy} - {allergy_descriptions.get(allergy, '📌 설명 없음')}"
            for allergy in matched_allergies
        ]
        return ", ".join(allergy_list)

    return "✅ 안전합니다! 감지된 알러지가 없습니다."
