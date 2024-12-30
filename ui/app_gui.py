# ui/app_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modules.chatgpt_api import ChatGPTClient
from modules.wordpress_api import WordPressClient
from modules.text_generator import TextGenerator


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WordPress Auto Publisher (XML-RPC) with Images")

        # 메인 윈도우가 리사이즈될 때, 내부 위젯도 확장되도록 설정
        self.root.rowconfigure(3, weight=1)  # 글 내용 미리보기 영역이 있는 row
        self.root.columnconfigure(1, weight=1)  # 텍스트 위젯이 있는 column

        # 모듈 인스턴스화
        self.chatgpt_client = ChatGPTClient()
        self.wp_client = WordPressClient()
        self.text_generator = TextGenerator()

        # 이미지 파일 경로들을 담는 리스트
        self.selected_images = []

        # GUI 구성
        self.create_widgets()

    def create_widgets(self):
        # ========== 키워드 입력 영역 ==========
        keyword_label = ttk.Label(self.root, text="키워드 (쉼표 구분):")
        keyword_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.keyword_entry = ttk.Entry(self.root, width=40)
        self.keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # ========== GPT 프롬프트 입력 ==========
        prompt_label = ttk.Label(self.root, text="GPT에게 보낼 프롬프트:")
        prompt_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.prompt_text = tk.Text(self.root, width=60, height=5)
        self.prompt_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)

        # ========== 이미지 관리 영역 ==========
        image_frame = ttk.LabelFrame(self.root, text="이미지 목록")
        image_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 내부에도 확장 설정
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)

        # 이미지 목록 리스트박스
        self.image_listbox = tk.Listbox(image_frame, height=5, width=50)
        self.image_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

        # 스크롤바
        scrollbar = ttk.Scrollbar(image_frame, orient="vertical", command=self.image_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.image_listbox.config(yscrollcommand=scrollbar.set)

        # 버튼들(추가/삭제)
        image_button_frame = ttk.Frame(image_frame)
        image_button_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N)

        add_image_button = ttk.Button(image_button_frame, text="이미지 추가", command=self.add_image)
        add_image_button.pack(pady=2)

        remove_image_button = ttk.Button(image_button_frame, text="이미지 삭제", command=self.remove_image)
        remove_image_button.pack(pady=2)

        # ========== 글 미리보기 ==========
        content_preview_label = ttk.Label(self.root, text="글 내용 미리보기:")
        content_preview_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.NW)

        # height 값을 15 정도로 키움
        self.content_preview_text = tk.Text(self.root, width=60, height=15)
        # sticky로 상하좌우(nsew)에 다 붙도록 설정
        self.content_preview_text.grid(row=3, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # ========== 버튼: 글 생성 / 업로드 ==========
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.E)

        generate_button = ttk.Button(button_frame, text="ChatGPT 글 생성", command=self.generate_post)
        generate_button.pack(side=tk.LEFT, padx=5)

        publish_button = ttk.Button(button_frame, text="WordPress 업로드", command=self.publish_post)
        publish_button.pack(side=tk.LEFT, padx=5)

    # ---------------------------------------------------------
    #                이미지 추가/삭제 메서드
    # ---------------------------------------------------------
    def add_image(self):
        """이미지 파일을 선택해 리스트에 추가"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        paths = filedialog.askopenfilenames(title="이미지 파일 선택", filetypes=filetypes)
        if paths:
            for p in paths:
                self.selected_images.append(p)
                self.image_listbox.insert(tk.END, p)

    def remove_image(self):
        """선택된 이미지를 리스트에서 제거"""
        sel = self.image_listbox.curselection()
        if not sel:
            messagebox.showwarning("경고", "삭제할 이미지를 선택하세요.")
            return
        for idx in reversed(sel):
            self.selected_images.pop(idx)
            self.image_listbox.delete(idx)

    # ---------------------------------------------------------
    #                글 생성 메서드 (ChatGPT)
    # ---------------------------------------------------------
    def generate_post(self):
        keywords_str = self.keyword_entry.get().strip()
        prompt = self.prompt_text.get("1.0", tk.END).strip()

        if not prompt:
            messagebox.showwarning("경고", "프롬프트를 입력하세요.")
            return

        image_count = len(self.selected_images)

        system_message = (
            "You are a helpful assistant. "
            f"We have {image_count} images that can be placed in the post. "
            "Please insert placeholders like [IMAGE:1], [IMAGE:2], ... in the content. "
            "Use them in a sensible way."
        )
        full_prompt = f"{system_message}\n\nUser Prompt: {prompt}"
        generated_content = self.chatgpt_client.generate_content(full_prompt)

        if not generated_content:
            messagebox.showerror("에러", "글 생성에 실패했습니다.")
            return

        # 제목 자동 생성
        keywords_list = [kw.strip() for kw in keywords_str.split(",") if kw.strip()]
        title = self.text_generator.generate_title_from_keywords(keywords_list)

        # 본문 후처리
        finalized_content = self.text_generator.finalize_content(generated_content)

        # 미리보기
        preview_text = f"제목: {title}\n\n{finalized_content}"
        self.content_preview_text.delete("1.0", tk.END)
        self.content_preview_text.insert("1.0", preview_text)

        messagebox.showinfo("알림", "글이 생성되었습니다. 내용을 확인 후 업로드하세요.")

    # ---------------------------------------------------------
    #                게시글 업로드 메서드
    # ---------------------------------------------------------
    def publish_post(self):
        full_text = self.content_preview_text.get("1.0", tk.END).strip()
        if not full_text:
            messagebox.showwarning("경고", "업로드할 글이 없습니다.")
            return

        try:
            first_line, content_lines = full_text.split("\n", 1)
            title = first_line.replace("제목: ", "").strip()
            content = content_lines.strip()
        except ValueError:
            messagebox.showerror("에러", "제목을 추출할 수 없습니다. '제목: ' 포맷인지 확인해주세요.")
            return

        if len(self.selected_images) > 0:
            image_urls = self.wp_client.upload_images(self.selected_images, title_prefix=title)
            for idx, img_url in enumerate(image_urls, start=1):
                placeholder = f"[IMAGE:{idx}]"
                img_tag = f'<p><img src="{img_url}" alt="image{idx}" /></p>'
                content = content.replace(placeholder, img_tag)

        categories = ["워드프레스"]
        tags = ["XML-RPC", "여러이미지"]

        post_id = self.wp_client.create_post(
            title=title,
            content=content,
            categories=categories,
            tags=tags,
            status="publish"
        )

        if post_id:
            messagebox.showinfo("성공", f"게시글 업로드 완료! (Post ID: {post_id})")
        else:
            messagebox.showerror("에러", "게시글 업로드에 실패했습니다.")
