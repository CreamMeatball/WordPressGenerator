# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에 정의된 환경변수 로드

# OpenAI API 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY')
GPT_MODEL = "gpt-4o"
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# WordPress 설정
WORDPRESS_SITE_URL = os.getenv('WORDPRESS_SITE_URL', 'https://your-wordpress-site.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'admin')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD', 'your_password')

# 그 외 설정
MAX_TOKENS = 2000
TEMPERATURE = 0.7
