# 환경 변수 관리
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def get_env_var(var_name: str):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"{var_name} 환경 변수가 설정되지 않았습니다.")
    return value
