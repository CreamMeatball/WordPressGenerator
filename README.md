# WordPress Auto Publisher with GPT & Images

> ChatGPT를 통해 자동 생성된 글을, XML-RPC를 통해 WordPress.com(또는 Self-Hosted WordPress)에 업로드할 수 있는 Python 기반 데스크톱 GUI 프로그램입니다.

## 목차
- [WordPress Auto Publisher with GPT \& Images](#wordpress-auto-publisher-with-gpt--images)
  - [목차](#목차)
  - [프로그램 개요](#프로그램-개요)
    - [주요 의의](#주요-의의)
  - [프로그램 기능](#프로그램-기능)
  - [프로젝트 구조](#프로젝트-구조)
    - [주요 파일 설명](#주요-파일-설명)
  - [사용 방법](#사용-방법)
  - [주의사항](#주의사항)
  - [라이선스](#라이선스)

---

## 프로그램 개요

- **ChatGPT API**(OpenAI)와 **WordPress XML-RPC**를 활용하여, 사용자 입력(키워드/프롬프트)에 기반한 글을 자동 생성하고, 선택한 이미지를 포함하여 WordPress에 게시합니다.  
- Tkinter GUI로 구현되어 있어, **키워드**, **프롬프트**, **이미지**를 직관적으로 추가/삭제/수정할 수 있습니다.  

### 주요 의의
1. **반복 업무 자동화**: 블로그나 사이트에 많은 글을 올려야 할 때, GPT를 통해 초안을 생성하고, GUI에서 내용을 확인 후 바로 게시 가능  
2. **이미지 업로드**: 여러 장의 이미지를 한 번에 업로드하고, 본문 내 원하는 위치(placeholder)에 삽입  
3. **유연한 구조**: ChatGPT API, WordPress XML-RPC 로직, GUI가 모듈 단위로 분리되어 있어 확장/유지보수 용이  

---

## 프로그램 기능

1. **키워드 기반 제목 자동 생성**  
   - 입력한 키워드로부터 자동으로 제목(`generate_title_from_keywords`)을 생성  
2. **ChatGPT 글 생성**  
   - 사용자 프롬프트를 GPT에 전달하여 초안(본문)을 생성  
   - 글의 마지막에 특정 문구를 추가하거나, 필요 시 추가 후처리를 함  
3. **이미지 추가/삭제 & 업로드**  
   - GUI에서 **파일 선택** 다이얼로그로 여러 장의 이미지를 등록 가능  
   - 업로드 시 **XML-RPC**로 한 장씩 업로드 후, 본문 내 `[IMAGE:1], [IMAGE:2]...` placeholder를 `<img src="...">` 태그로 치환  
4. **WordPress 게시글 자동 업로드**  
   - 글 제목 / 본문 / 카테고리 / 태그 / 썸네일(선택) 등 한 번에 등록  
   - 게시글 ID를 받아, 업로드 성공 여부를 확인 가능  
5. **GUI에서 창 크기 조절**  
   - 창 크기에 따라 **글 미리보기 영역** 등 위젯이 자동으로 확장됨  

---

## 프로젝트 구조

```
my_wordpress_automation/
├── main.py                   # 실행 진입점
├── requirements.txt          # 필요한 라이브러리 목록
├── .env                      # 사용자가 생성 필요. API Key, ID, Password..
├── config/
│   └── config.py             # 환경 변수, API 키, 워드프레스 URL/계정 정보
├── modules/
│   ├── chatgpt_api.py        # OpenAI GPT API 연동 (글 생성)
│   ├── wordpress_api.py      # WordPress XML-RPC 연동 (이미지, 포스트 업로드)
│   └── text_generator.py     # GPT 응답 후처리(제목 생성, 마무리 문구 등)
└── ui/
    └── app_gui.py            # Tkinter GUI (사용자 입력, 이벤트 처리)
```

### 주요 파일 설명

- **`main.py`**  
  - 전체 프로그램 실행의 진입점. Tkinter 윈도우를 띄우고 GUI를 구동함.  
- **`config/config.py`**  
  - `.env`에서 불러온 **OpenAI API 키**, **WordPress.com Application Password** 등 민감 정보를 관리.  
- **`modules/chatgpt_api.py`**  
  - **OpenAI**에서 제공하는 Python 라이브러리(1.58.1 이상)를 통해 GPT 호출.  
  - `generate_content(prompt)` 함수로 프롬프트 → GPT 응답(본문)  
- **`modules/wordpress_api.py`**  
  - **`python-wordpress-xmlrpc`** 라이브러리로 XML-RPC 업로드 처리.  
  - `upload_images()` / `create_post()` 함수를 제공  
- **`modules/text_generator.py`**  
  - GPT 응답 후처리. 예: 제목 자동 생성, 글 하단에 문구 추가 등.  
- **`ui/app_gui.py`**  
  - **Tkinter** 기반 GUI. 키워드/프롬프트 입력, 이미지 추가/삭제, 글 생성/업로드 버튼, 글 미리보기 등을 담당.  

---

## 사용 방법

1. **파이썬 환경 구성**  
   - Python 3.9 이상 권장  
   - 가상환경(venv) 사용을 추천
2. **라이브러리 설치**  
   ```bash
   pip install -r requirements.txt
   ```
   > `requirements.txt`에 다음 라이브러리가 포함되어 있어야 합니다.  
   > - openai==1.58.1
   > - requests==2.32.2
   > - python-dotenv==1.0.1
   > - tk==0.1.0
   > - python-wordpress-xmlrpc==2.3
   > - datetime==5.5
   > - pytz==2024.2
   > - 등등
3. **.env 설정**   
   - **.env 파일 생성**:
     - 프로젝트 루트 디렉토리에 '.env' 파일 생성
   - **.env 내용 양식**:  
     - `OPENAI_API_KEY=sk-...`
     - `WORDPRESS_SITE_URL=https://<내블로그>.wordpress.com/xmlrpc.php`  
     - `WORDPRESS_USERNAME=<내 워드프레스 계정(이메일)>`  
     - `WORDPRESS_PASSWORD=<워드프레스 비밀번호>`  
4. **프로그램 실행**  
   ```bash
   python main.py
   ```
5. **GUI 사용**  
   - `키워드` 입력 (예: `파이썬, 자동 포스팅`)  
   - `GPT에게 보낼 프롬프트` 입력 (예: "파이썬 활용법에 대한 글 작성해줘")  
   - 필요한 경우 `이미지 추가`로 이미지 선택  
   - **[ChatGPT 글 생성]** 클릭 → 미리보기 창에 제목/본문 생성  
   - 필요 시 미리보기 내용 수정  
   - **[WordPress 업로드]** 클릭 → 자동 게시 (이미지 포함)  

---

## 주의사항

1. **WordPress.com vs. Self-Hosted WordPress**  
   - WordPress.com( \*.wordpress.com ) 환경에서는 XML-RPC 접근 시, **Application Password**가 필요.  
   - 일반적인 Basic Auth(계정명+비번)으로는 404 또는 인증 에러 발생 가능.  
2. **이미지 업로드 제한**  
   - 무료 플랜의 경우, 업로드 가능한 이미지 용량/트래픽이 제한될 수 있음.  
3. **OpenAI API 사용 비용**  
   - GPT-4 등의 모델을 사용할 경우, **토큰 단가**가 높습니다. (사용량에 따라 과금)  
   - 꼭 **사용량 모니터링**을 권장합니다.  
4. **ChatGPT 응답 품질**  
   - GPT 모델, 프롬프트 설계, 토큰 제한 등에 따라 글 품질이 달라집니다.  
   - 자동 생성된 글은 **반드시** 인간 검수 과정을 거쳐, 표절/정확도 문제 등을 점검해주세요.  
5. **XML-RPC 활성화**  
   - Self-Hosted 워드프레스라면, 일부 호스팅/보안 플러그인이 `xmlrpc.php` 접근을 차단하기도 합니다.  
   - WordPress.com은 기본적으로 XML-RPC가 켜져 있지만, 상황에 따라 제한이 있을 수 있습니다.  
6. **저작권 및 윤리적 이슈**  
   - 자동 생성된 텍스트/이미지에 대한 저작권, 또는 가짜 뉴스, 개인정보 침해 등의 문제가 발생하지 않도록 유의하세요.  

---

## 라이선스

- 본 프로젝트의 소스코드는 [MIT License](https://opensource.org/licenses/MIT)와 같이 자유롭게 사용 가능하나,  
  **OpenAI API**와 **WordPress.com** 사용 시에는 각자의 [약관](https://openai.com/policies/terms-of-use), [제한](https://wordpress.com/tos)을 준수해야 합니다.  
- 해당 코드를 사용하는 과정에서 발생하는 모든 문제(데이터 누락, API 과금, 계정 제한, 윤리적 문제 등)에 대해서,  
  **개발자는 책임지지 않습니다.** 사용자는 충분한 테스트와 검토를 거쳐 운용해야 합니다.