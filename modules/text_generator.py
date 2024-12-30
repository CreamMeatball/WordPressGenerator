# modules/text_generator.py

class TextGenerator:
    """
    ChatGPT의 응답(글 내용)에 대해 추가적인 변형/가공 로직을 담당.
    예: 키워드 삽입, 제목 자동 생성, 마무리 멘트 추가 등
    """
    def __init__(self):
        pass

    def generate_title_from_keywords(self, keywords: list) -> str:
        """
        예시: 키워드를 받아서 기본적인 제목을 생성.
        키워드가 ['파이썬', '웹 크롤링'] 이면 -> '[파이썬, 웹 크롤링] 자동 생성 글'
        """
        joined_keywords = ", ".join(keywords)
        return f"[{joined_keywords}] 자동 생성 글"

    def finalize_content(self, content: str) -> str:
        """
        ChatGPT 결과물을 받아 최종적으로 약간의 수정 등을 하고
        HTML 태그나 문구를 추가할 수 있음.
        """
        # 예시: 글 하단에 '감사합니다!' 텍스트 추가
        final_content = content + "\n\n감사합니다!"
        return final_content
