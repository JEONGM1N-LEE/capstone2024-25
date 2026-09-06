# 백엔드 (FastAPI)

가공식품 성분표 이미지를 받아 Tesseract OCR로 읽고, PostgreSQL `allergy_synonyms` 테이블과 비교합니다.

프론트엔드의 `POST /scanner`가 이 서버의 `POST /ocr/`를 호출합니다.

## 요구 사항

- Python 3.11+
- PostgreSQL (`users_db`)
- Tesseract OCR + 한글 언어 데이터 (`kor`)
- 저장소 루트에서 실행 (패키지 import가 `backend.*` 기준)

Windows에 Tesseract를 기본 경로로 설치하면 별도 설정 없이 동작합니다.

`C:\Program Files\Tesseract-OCR\tesseract.exe`

다른 경로라면 `backend/.env`에 `TESSERACT_CMD`를 넣으세요.

## 설치

저장소 루트에서:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
```

`.venv/`는 Git에 포함하지 않습니다. 클론한 뒤 위처럼 다시 만들면 됩니다.

## 실행

```powershell
uvicorn backend.main:app --reload --port 8000
```

확인:

- [http://localhost:8000](http://localhost:8000) → 서버 기동 메시지
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

CORS는 `http://localhost:5173`만 허용합니다.

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 헬스 체크 |
| `POST` | `/ocr/` | `file` 필드로 이미지 업로드. OCR 후 알레르기 매칭 결과를 `{ "warning": "..." }`로 반환 |

`/check-allergy/`, `/chat/` 라우트는 코드에 있으나 `main.py`에 아직 등록되어 있지 않습니다. 실제 챗봇은 프론트엔드 `/api/chat` (Groq)을 사용합니다.

## 데이터베이스

SQLAlchemy가 `allergy_synonyms` 테이블을 읽습니다.

| 컬럼 | 의미 |
|------|------|
| `allergy_name` | 대표 알레르기 이름 |
| `synonym` | 쉼표로 구분한 동의어 |
| `description` | 사용자에게 보여줄 설명 |

연결 정보는 `backend/database.py`의 `DATABASE_URL`입니다. Prisma 사용자 테이블과 같은 DB를 쓰는 구성입니다.

## 폴더

```
backend/
├── main.py              # FastAPI 앱, CORS, 라우터 등록
├── database.py          # PostgreSQL 세션
├── requirements.txt
├── models/allergy.py    # allergy_synonyms ORM
├── routes/ocr.py        # POST /ocr/
├── services/ocr_service.py
└── services/db_service.py
```
