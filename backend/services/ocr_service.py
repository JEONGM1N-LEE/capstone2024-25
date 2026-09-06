# 필수
import os
import pytesseract
from PIL import Image
from sqlalchemy.orm import Session
from backend.services.db_service import find_matching_allergies

DEFAULT_TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class OCRService:
    def __init__(self, tesseract_cmd=None):
        cmd = tesseract_cmd or os.getenv("TESSERACT_CMD")
        if not cmd and os.path.exists(DEFAULT_TESSERACT_CMD):
            cmd = DEFAULT_TESSERACT_CMD
        if cmd:
            pytesseract.pytesseract.tesseract_cmd = cmd

    def extract_text(self, image_path: str) -> str:
        """이미지에서 텍스트 추출 (예외 처리 추가)"""
        try:
            if not os.path.exists(image_path):
                return "🚨 오류: 이미지 파일을 찾을 수 없습니다."

            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="kor+eng")
            return text.strip()
        except Exception as e:
            return f"🚨 OCR 오류: {str(e)}"

    def detect_allergies(self, db: Session, image_path: str):
        """OCR 후 알러지 성분 감지"""
        text = self.extract_text(image_path)
        if text.startswith("🚨"):
            return text
        if not text:
            return "🚨 OCR 오류: 이미지에서 글자를 읽지 못했습니다."

        matched_allergies = find_matching_allergies(db, text)
        if matched_allergies.startswith("🚨"):
            return matched_allergies
        if "✅ 안전합니다!" in matched_allergies:
            return matched_allergies
        return f"🚨 알러지 주의: {matched_allergies}"
