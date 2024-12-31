# modules/wordpress_api.py

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.compat import xmlrpc_client
import os

from config.config import (
    WORDPRESS_SITE_URL,
    WORDPRESS_USERNAME,
    WORDPRESS_PASSWORD
)

class WordPressClient:
    def __init__(self):
        self.client = Client(
            WORDPRESS_SITE_URL,
            WORDPRESS_USERNAME,
            WORDPRESS_PASSWORD
        )

    def upload_images(self, image_paths, title_prefix=""):
        """
        여러 이미지 파일을 XML-RPC로 업로드하고,
        업로드된 각 이미지의 URL 리스트를 반환.
        """
        urls = []
        for idx, path in enumerate(image_paths, start=1):
            if not os.path.exists(path):
                print(f"[WordPressClient] 이미지 경로 오류: {path}")
                continue

            ext = os.path.splitext(path)[1].lower()
            mime_type = "image/jpeg"
            if ext == ".png":
                mime_type = "image/png"
            elif ext in [".gif"]:
                mime_type = "image/gif"
            elif ext in [".bmp"]:
                mime_type = "image/bmp"

            with open(path, "rb") as img_file:
                image_data = img_file.read()

            data = {
                "name": f"{title_prefix}_{idx}{ext}",  # 예: "게시글제목_1.png"
                "type": mime_type,
                "bits": xmlrpc_client.Binary(image_data),
                "overwrite": False,
            }

            try:
                response = self.client.call(UploadFile(data))
                # response 예시: {'id': 123, 'file': '...', 'url': 'http://...', 'type': 'image/png'}
                url = response.get("url")
                if url:
                    urls.append(url)
            except Exception as e:
                print("[WordPressClient] 이미지 업로드 실패:", e)

        return urls

    def create_post(self, title, content, categories=None, tags=None, status="draft"):
        if categories is None:
            categories = []
        if tags is None:
            tags = []

        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = status
        post.terms_names = {
            "category": categories,
            "post_tag": tags
        }

        try:
            post_id = self.client.call(NewPost(post))
            return post_id
        except Exception as e:
            print("[Error in WordPressClient.create_post]", e)
            return None
