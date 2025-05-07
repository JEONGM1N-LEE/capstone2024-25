# 필수
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse  # 🚨 JSONResponse import 추가
import shutil
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.ocr_service import OCRService

router = APIRouter()
ocr_service = OCRService()

# 절대 경로로 폴더를 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")  # 백엔드 루트의 uploads 폴더 지정
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 폴더가 없으면 자동 생성

# OCR 결과를 DB와 연결하여 알러지 감지 기능 추가

@router.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="🚨 파일이 전달되지 않았습니다.")  # 🚨 파일이 없으면 400 오류 반환
    """ 사용자가 업로드한 이미지를 OCR 처리하고 알러지 감지 """
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as file_object:
            shutil.copyfileobj(file.file, file_object)

        allergies = ocr_service.detect_allergies(db, file_location)
        # warning_message = allergies if isinstance(allergies, str) else allergies.get("warning", "🚨 알러지 감지 오류")

        # 🚀 `matched_allergies` 내부 키 제거 후 바로 경고 메시지 반환
        # if isinstance(allergies, dict) and "matched_allergies" in allergies:
        #         warning_message = allergies["matched_allergies"]
        # else:
        #     warning_message = allergies  # 이미 문자열이면 그대로 사용

        return JSONResponse(content={"warning": allergies})
    #     return JSONResponse(content={"warning": warning_message})
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"OCR 처리 오류: {str(e)}")

        # return JSONResponse(content={"warning": str(warning_message)})  # ✅ 깔끔한 응답 반환

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 처리 오류: {str(e)}")
