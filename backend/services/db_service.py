# PostgreSQL 데이터베이스에서 알러지 성분 검색
# OCR로 추출된 텍스트에서 데이터베이스의 알러지 성분과 일치하는 단어를 찾는 기능 추가!
from sqlalchemy.orm import Session
from backend.models.allergy import AllergySynonyms

def find_matching_allergies(db: Session, text: str):
    """ OCR 결과에서 알러지 성분과 일치하는 항목 찾기 """
    words = text.lower().split()  # OCR 결과를 단어 리스트로 변환
    matched_allergies = set()  # 🚀 중복 제거를 위해 set() 사용
    allergy_descriptions = {}

    # DB에서 알러지 성분 검색
    allergies = db.query(AllergySynonyms).all()

    for allergy in allergies:
        synonyms_list = allergy.synonym.split(",")  # 동의어를 리스트로 변환
        all_names = [allergy.allergy_name] + synonyms_list  # 기본 이름과 동의어 리스트를 결합
        if any(word.strip() in all_names for word in words):
            matched_allergies.add(allergy.allergy_name)  # 🚀 set()을 사용해 중복 추가 방지
            allergy_descriptions[allergy.allergy_name] = getattr(allergy, "description", "📌 설명 없음")  # 🚀 안전하게 속성 가져오기
            # allergy_descriptions[allergy.allergy_name] = allergy.description if allergy.description else "📌 설명 없음" # 🚀 설명 추가
            # matched_allergies.append(allergy.allergy_name)

    # 감지된 알러지 성분이 있으면 경고 문구 생성
    if matched_allergies:
        allergy_list = [f"{allergy} - {allergy_descriptions.get(allergy, '📌 설명 없음')}" for allergy in matched_allergies]
        return ", ".join(allergy_list)
        # warnings = [
        #     f"🚨 알러지 주의: {allergy} - {allergy_descriptions.get(allergy, '📌 설명 없음')}"
        #     for allergy in matched_allergies
        # ]
        # return " | ".join(warnings)  # 🚀 설명을 포함한 경고 메시지 반환

    # if matched_allergies:
    #     return f"🚨 알러지 주의: {', '.join(matched_allergies)}"

    return "✅ 안전합니다! 감지된 알러지가 없습니다."
