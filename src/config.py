import os
from google.generativeai import GenerativeModel, GenerationConfig

# 환경 변수에서 API 키를 불러오고, 쉼표로 구분된 값을 리스트로 변환
API_KEYS = os.getenv('API_KEYS', '').split(',')

# 모델 설정
model_name = 'gemini-1.5-flash'
generation_config = GenerationConfig(
    temperature=0.7,          # 생성된 텍스트의 창의성 정도 (0.0~1.0)
    top_k=10,                 # 상위 K개의 후보 단어 중에서 선택
    max_output_tokens=5000    # 생성할 최대 토큰 수
)

# 기본 봇 설정 (공통 설정)
default_bot_settings = {
    'max_run_time': 1800,                 # 최대 실행 시간 (초)
    'article_interval': 600,              # 기사 작성 간격 (초)
    'comment_interval': 22,               # 댓글 작성 간격 (초)
    'crawl_article_count': 20,            # 크롤링할 기사 수
    'comment_target_count': 20,           # 댓글을 달 대상 수
    'write_article_enabled': False,       # 기사 작성 활성화 여부
    'write_comment_enabled': True,        # 댓글 작성 활성화 여부
    'record_memory_enabled': True,        # 메모리 기록 활성화 여부
    'record_data_enabled': True,          # 데이터 기록 활성화 여부
    'use_time_limit': False,              # 시간 제한 사용 여부
    'load_memory_enabled': True,          # 메모리 로드 활성화 여부
    'load_data_enabled': True,            # 데이터 로드 활성화 여부
    'gallery_record_interval': 600,       # 갤러리 기록 간격 (초)
    'username': 'ㅇㅇ',                    # 사용자 이름
    'password': '12345',                  # 비밀번호 (보안상의 이유로 암호화 추천)
    'persona': "무뚝뚝한 성격의 마음은 따뜻한 여자 고등학생", # 봇의 성격
}
