# 디시인사이드 갤러리 봇

이 봇은 특정 디시인사이드 갤러리에 댓글을 자동으로 작성하는 봇입니다. 구글의 생성 AI 모델을 사용하여 댓글을 생성합니다.

## 개요

이 프로젝트는 디시인사이드 만화 갤러리와 상호 작용하는 봇을 구현합니다. 이 봇은 구글 생성 AI 모델을 사용하여 지정된 페르소나에 따라 댓글을 생성합니다. 최신 게시물을 자동으로 크롤링하고, 사전 설정된 설정에 따라 댓글을 게시할 수 있습니다.

## 기능

- 지정된 디시인사이드 갤러리의 최신 게시물을 자동으로 크롤링합니다.
- 구글 생성 AI 모델을 사용하여 댓글을 생성합니다.
- 선택된 게시물에 댓글을 게시합니다.
- 페르소나, 간격, 제한 등을 설정할 수 있습니다.

## 설정

### 환경 변수

Google API 키를 환경 변수로 설정하세요:

```sh
export GOOGLE_API_KEY=your_google_api_key
```

### 설정 파일

config.py에서 봇 설정을 구성하세요:

```python
import os
import google.generativeai as genai

# 설정 상수
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # API 키를 환경 변수로 설정
BOARD_ID = 'your_board_id'  # 갤러리 ID
USERNAME = 'your_username'  # 사용자명
PASSWORD = 'your_password'  # 비밀번호
PERSONA = """
I am the "Official #1 Fan of Kim Hoya" who fervently likes Kim Hoya.
I am active in the DC Inside Comic Gallery and aim to spread Kim Hoya's humor.
I always communicate cheerfully using the unique language style of DC Inside.
I do not use symbols, and all writings are in Korean.
"""
MAX_RUN_TIME = 1800  # 최대 실행 시간 (초)
COMMENT_INTERVAL = 30  # 댓글 작성 간격 (초)
CRAWL_ARTICLE_COUNT = 20  # 크롤링할 글 개수
COMMENT_TARGET_COUNT = 15  # 댓글 대상 글 개수
WRITE_COMMENT_ENABLED = True  # 댓글 활성화 여부
USE_TIME_LIMIT = False  # 시간 제한 사용 여부

# Google API 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
generation_config = genai.GenerationConfig(
    temperature=0.6,
    top_k=1,
    max_output_tokens=750
)
```

### 설치

필요한 패키지를 설치하세요:

```sh
pip install -r requirements.txt -q
```

## 봇 실행

아래 명령어로 봇을 실행하세요:

```sh
python main.py
```
