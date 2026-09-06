# 백엔드 (FastAPI)

가공식품 성분표 이미지를 받아 Tesseract OCR(`kor+eng`)로 읽고, 식약처 라벨의 **함유** 구간만 PostgreSQL `allergy_synonyms`와 비교합니다.

프론트엔드의 `POST /scanner`가 이 서버의 `POST /ocr/`를 호출합니다.

## 요구 사항

- Python 3.11+
- PostgreSQL (`users_db`)
- Tesseract OCR + 한글 언어 데이터 (`kor`)
- 저장소 **루트**에서 실행 (패키지 import가 `backend.*` 기준)

Windows에 Tesseract를 기본 경로로 설치하면 별도 설정 없이 동작합니다.

`C:\Program Files\Tesseract-OCR\tesseract.exe`

다른 경로라면 `backend/.env`에 `TESSERACT_CMD`를 넣으세요.

## 설치

저장소 루트에서:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

CMD에서는 `.ps1`이 메모장으로 열릴 수 있습니다.

```cmd
.venv\Scripts\activate.bat
```

활성화 없이 실행하려면:

```cmd
.venv\Scripts\uvicorn.exe backend.main:app --reload --port 8000
```

`.venv/`는 Git에 포함하지 않습니다. 클론한 뒤 위처럼 다시 만들면 됩니다.

## 실행

루트에서:

```powershell
uvicorn backend.main:app --reload --port 8000
```

`backend` 폴더에서 `uvicorn main:app`을 치면 `from backend.xxx` import가 실패합니다.

확인:

- [http://localhost:8000](http://localhost:8000) → 서버 기동 메시지
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

CORS는 `http://localhost:5173`만 허용합니다.

## API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/` | 헬스 체크 |
| `POST` | `/ocr/` | `file` 필드로 이미지 업로드. OCR 후 문장형 안내를 `{ "warning": "..." }`로 반환 |

`/check-allergy/`, `/chat/` 라우트는 코드에 있으나 `main.py`에 아직 등록되어 있지 않습니다. 실제 챗봇은 프론트엔드 `/api/chat` (Groq)을 사용합니다.

## 매칭 로직

`services/db_service.py`가 OCR 텍스트를 구간으로 나눕니다.

1. `혼입 가능`, `같은 제조시설` 이후는 버림
2. `함유` 바로 앞 목록만 알레르기 이름/동의어와 비교
3. `제품명`을 찾으면 답변에 넣고, 없으면 “가공식품”
4. 매칭된 각 성분의 `warning` 컬럼으로 주의 문장을 붙임

답변 예:

```
올려주신 사진 속 제품은 초코칩쿠키로 보입니다.
이 제품에 함유된 알레르기 성분은 밀, 알류, 우유, 대두, 쇠고기입니다.

각 성분에 대한 주의사항은 아래와 같습니다.
• 밀: ...
```

`함유`를 못 읽으면 라벨 전체를 맞추지 않고, 함유 표시를 찾지 못했다고만 안내합니다.

## 데이터베이스

SQLAlchemy가 `allergy_synonyms` 테이블을 읽습니다.

| 컬럼 | 의미 |
|------|------|
| `allergy_name` | 대표 알레르기 이름 (알류, 우유, 밀 등) |
| `synonym` | 쉼표로 구분한 동의어 (달걀, 난황, 밀가루 등) |
| `description` | 보조 설명 (`warning`이 없을 때 사용) |
| `warning` | 사용자에게 보여줄 주의 문구 |

연결 정보는 `backend/database.py`의 `DATABASE_URL`입니다. Prisma 사용자 테이블과 같은 DB를 쓰는 구성입니다.

`warning` 컬럼이 없다면:

```sql
ALTER TABLE allergy_synonyms
ADD COLUMN IF NOT EXISTS warning VARCHAR;
```

그다음 성분별 `UPDATE ... SET warning = '...'`로 문장을 채우세요.

## 폴더

```
backend/
├── main.py                 # FastAPI 앱, CORS, 라우터 등록
├── database.py             # PostgreSQL 세션
├── requirements.txt
├── models/allergy.py       # allergy_synonyms ORM
├── routes/ocr.py           # POST /ocr/
├── services/ocr_service.py # Tesseract kor+eng
└── services/db_service.py  # 함유 구간 매칭 + 문장 조립
```
