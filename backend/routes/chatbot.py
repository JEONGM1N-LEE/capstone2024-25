# 사용자의 입력을 받아 OpenAI API로 처리한 후 결과를 반환하는 라우트를 작성

from fastapi import APIRouter
from backend.services.openai_service import process_user_input

router = APIRouter()

@router.post("/chat/")
async def chat_with_bot(user_input: str):
    """
    사용자의 입력을 받아 OpenAI 모델로 처리한 후 결과 반환.
    """
    response = await process_user_input(user_input)
    return {"response": response}
