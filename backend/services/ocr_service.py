# 필수
import os
import pytesseract
from PIL import Image
from sqlalchemy.orm import Session
from backend.services.db_service import find_matching_allergies

class OCRService:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image_path: str) -> str:
        """ 이미지에서 텍스트 추출 (예외 처리 추가) """
        try:
            if not os.path.exists(image_path):
                return "🚨 오류: 이미지 파일을 찾을 수 없습니다."

            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="kor")  # 한국어 OCR 지원
            return text.strip()
        except Exception as e:
            return f"🚨 OCR 오류: {str(e)}"

    def detect_allergies(self, db: Session, image_path: str):
        """ OCR 후 알러지 성분 감지 """
        text = self.extract_text(image_path)
        matched_allergies = find_matching_allergies(db, text)
        return f"🚨 알러지 주의: {matched_allergies}" if "✅ 안전합니다!" not in matched_allergies else matched_allergies

        # return f"🚨 알러지 주의: {', '.join(matched_allergies)}" if matched_allergies else "✅ 안전합니다!"
        # return {"matched_allergies": matched_allergies}

# OCR 결과를 DB와 비교하는 로직 추가

