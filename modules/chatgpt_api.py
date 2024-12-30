# modules/chatgpt_api.py

import os
from openai import OpenAI
from config.config import OPENAI_API_KEY, GPT_MODEL, MAX_TOKENS, TEMPERATURE

class ChatGPTClient:
    def __init__(self):
        # 추천 방식: 인스턴스화
        self.client = OpenAI(
            api_key=OPENAI_API_KEY  # 환경변수나 config에서 가져온 key
        )

    def generate_content(self, prompt: str) -> str:
        """
        ChatGPT에게 프롬프트를 보내고, 응답을 받아서 문자열로 반환.
        """
        try:
            response = self.client.chat.completions.create(
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a popular blogger. \
                        Always return your answer in valid HTML format and show only the content in <body> tag. No <head>, <style> content etc. No markdown, no ### or ** ** syntax. Use <h1>, <h2>, <p>, <strong>, etc. \
                        Write what you want in detail, long, and pretty ways, just like your popular blog post. \
                        The way you speak should be kind, too."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            # 결과 메시지 추출
            result = response.choices[0].message.content
            return result
        except Exception as e:
            print(f"[Error in ChatGPTClient] {e}")
            return ""
