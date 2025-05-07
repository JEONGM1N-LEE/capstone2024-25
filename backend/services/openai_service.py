# OpenAI API 호출 로직
import openai
from backend.utils.env_loader import get_env_var

# OpenAI API 키 설정
openai.api_key = get_env_var("OPENAI_API_KEY")

async def process_user_input(user_input: str):
    try:
        # 최신 메서드 사용 (GPT-4o Mini 모델)
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",  # 사용 중인 모델 이름
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in food allergen detection."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,  # 생성할 텍스트 길이 제한
            temperature=0.7  # 응답의 창의성 정도
        )
        # 응답 반환
        return response['choices'][0]['message']['content']
    except Exception as e:
        return {"error": str(e)}

# async def get_allergen_info(image_url: str):
#     try:
#         # OpenAI API 호출
#         response = openai.Image.create_recognition_request(image_url)
#         text = response.get("text", "")
#
#         # 알레르기 성분 목록과 매칭
#         allergens = ["달걀", "우유", "밀", "땅콩", "대두"]  # 알레르기 목록 업데이트
#         detected_allergens = [allergen for allergen in allergens if allergen in text]
#
#         return {"text": text, "allergens": detected_allergens}
#     except Exception as e:
#         return {"error": str(e)}

