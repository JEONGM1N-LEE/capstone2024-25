# PostgreSQL 데이터베이스에서 알러지 성분 검색
import re
from sqlalchemy.orm import Session
from backend.models.allergy import AllergySynonyms

MAY_CONTAIN_PATTERN = re.compile(
    r"(혼입\s*가능|혼입될\s*우려|같은\s*제조시설|동일\s*제조시설|"
    r"사용한\s*제품과\s*같은|제조시설에서\s*제조)",
    re.IGNORECASE,
)
CONTAINS_MARKER = re.compile(r"함\s*유|항유|함류")
PRODUCT_NAME_PATTERN = re.compile(
    r"(?:제품명|제품\s*명)\s*[:：]?\s*([^\n]+)",
    re.IGNORECASE,
)


def _normalize(text: str) -> str:
    return re.sub(r"[\s,./()\[\]:：·•\-_+]", "", (text or "")).lower()


def _term_in_text(normalized: str, term: str) -> bool:
    key = (term or "").strip().lower()
    if not key or key not in normalized:
        return False
    if key == "밀":
        masked = normalized.replace("밀크", "").replace("milk", "")
        return "밀" in masked
    return True


def _extract_product_name(text: str) -> str:
    match = PRODUCT_NAME_PATTERN.search(text or "")
    if not match:
        return "가공식품"
    name = re.sub(r"\s+", " ", match.group(1)).strip(" :：-/|")
    name = re.split(r"(식품유형|업소명|원재료|제조원|유통기한)", name)[0].strip()
    return name or "가공식품"


def _extract_contains_text(text: str) -> str | None:
    """혼입 가능 구간을 제외하고, '함유' 표시 근처 텍스트만 반환."""
    if not text:
        return None

    may_match = MAY_CONTAIN_PATTERN.search(text)
    scoped = text[: may_match.start()] if may_match else text

    chunks = []
    for match in CONTAINS_MARKER.finditer(scoped):
        before = scoped[: match.start()]
        prior_lines = [line.strip() for line in before.splitlines() if line.strip()]
        nearby = prior_lines[-1] if prior_lines else ""
        chunks.append(f"{nearby} {scoped[match.start():match.end()]}".strip())

    if not chunks:
        return None
    return " ".join(chunks)


def _match_allergies(db: Session, text: str):
    normalized = _normalize(text)
    matched = []
    seen = set()

    allergies = db.query(AllergySynonyms).all()
    for allergy in allergies:
        synonyms_list = [s.strip() for s in (allergy.synonym or "").split(",") if s.strip()]
        all_names = [allergy.allergy_name] + synonyms_list
        if any(_term_in_text(normalized, name) for name in all_names):
            if allergy.allergy_name in seen:
                continue
            seen.add(allergy.allergy_name)
            matched.append(allergy)
    return matched


def _particle_eulo(word: str) -> str:
    if not word:
        return "으로"
    last = word[-1]
    code = ord(last)
    if 0xAC00 <= code <= 0xD7A3 and (code - 0xAC00) % 28 != 0:
        return "으로"
    return "로"


def _format_result(product_name: str, matched) -> str:
    names = ", ".join(item.allergy_name for item in matched)
    particle = _particle_eulo(product_name)
    lines = [
        f"올려주신 사진 속 제품은 {product_name}{particle} 보입니다.",
        f"이 제품에 함유된 알레르기 성분은 {names}입니다.",
        "",
        "각 성분에 대한 주의사항은 아래와 같습니다.",
    ]
    for item in matched:
        caution = (item.warning or item.description or "알레르기 반응이 있을 수 있으니 주의하세요.").strip()
        lines.append(f"• {item.allergy_name}: {caution}")
    return "\n".join(lines)


def find_matching_allergies(db: Session, text: str):
    """함유 구간만 비교해 문장형 안내를 반환."""
    if (text or "").startswith("🚨"):
        return text
    if not (text or "").strip():
        return "🚨 OCR 오류: 이미지에서 글자를 읽지 못했습니다."

    product_name = _extract_product_name(text)
    contains_text = _extract_contains_text(text)

    intro = f"올려주신 사진 속 제품은 {product_name}{_particle_eulo(product_name)} 보입니다."

    if not contains_text:
        return (
            f"{intro}\n"
            "라벨에서 '함유' 표시를 찾지 못해, 확정된 알레르기 성분을 구분하지 못했습니다."
        )

    matched = _match_allergies(db, contains_text)
    if not matched:
        return (
            f"{intro}\n"
            "함유 표시에서 알레르기 성분이 확인되지 않았습니다."
        )

    return _format_result(product_name, matched)
