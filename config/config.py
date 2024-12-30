# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에 정의된 환경변수 로드

# OpenAI API 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
GPT_MODEL = "gpt-4o"
MAX_TOKENS = 2000 # 최대 토큰. 높을 수록 긴 글 생성
TEMPERATURE = 0.7 # 높을 수록 더 다양한 결과 생성

# WordPress 설정
WORDPRESS_SITE_URL = os.getenv('WORDPRESS_SITE_URL', 'https://your-wordpress-site.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'admin')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD', 'your_password')