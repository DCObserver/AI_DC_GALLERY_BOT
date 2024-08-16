import os
from dotenv import load_dotenv
from google.generativeai import GenerationConfig

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키를 불러오고, 쉼표로 구분된 값을 리스트로 변환
API_KEYS = os.getenv('API_KEYS', '').split(',')

# 모델 설정
MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-flash')
GENERATION_CONFIG = GenerationConfig(
    temperature=float(os.getenv('GEN_TEMPERATURE', 0.7)),  # 생성된 텍스트의 창의성 정도 (0.0~1.0)
    top_k=int(os.getenv('GEN_TOP_K', 10)),                # 상위 K개의 후보 단어 중에서 선택
    max_output_tokens=int(os.getenv('GEN_MAX_OUTPUT_TOKENS', 5000))  # 생성할 최대 토큰 수
)

# 기본 봇 설정 (공통 설정)
DEFAULT_BOT_SETTINGS = {
    'max_run_time': int(os.getenv('BOT_MAX_RUN_TIME', 1800)),         # 최대 실행 시간 (초)
    'article_interval': int(os.getenv('BOT_ARTICLE_INTERVAL', 600)),  # 기사 작성 간격 (초)
    'comment_interval': int(os.getenv('BOT_COMMENT_INTERVAL', 22)),   # 댓글 작성 간격 (초)
    'crawl_article_count': int(os.getenv('BOT_CRAWL_ARTICLE_COUNT', 20)),  # 크롤링할 기사 수
    'comment_target_count': int(os.getenv('BOT_COMMENT_TARGET_COUNT', 20)),  # 댓글을 달 대상 수
    'write_article_enabled': os.getenv('BOT_WRITE_ARTICLE_ENABLED', 'False') == 'True',  # 기사 작성 활성화 여부
    'write_comment_enabled': os.getenv('BOT_WRITE_COMMENT_ENABLED', 'True') == 'True',   # 댓글 작성 활성화 여부
    'record_memory_enabled': os.getenv('BOT_RECORD_MEMORY_ENABLED', 'True') == 'True',   # 메모리 기록 활성화 여부
    'record_data_enabled': os.getenv('BOT_RECORD_DATA_ENABLED', 'True') == 'True',     # 데이터 기록 활성화 여부
    'use_time_limit': os.getenv('BOT_USE_TIME_LIMIT', 'False') == 'True',                # 시간 제한 사용 여부
    'load_memory_enabled': os.getenv('BOT_LOAD_MEMORY_ENABLED', 'True') == 'True',       # 메모리 로드 활성화 여부
    'load_data_enabled': os.getenv('BOT_LOAD_DATA_ENABLED', 'True') == 'True',           # 데이터 로드 활성화 여부
    'gallery_record_interval': int(os.getenv('BOT_GALLERY_RECORD_INTERVAL', 600)),       # 갤러리 기록 간격 (초)
    'username': os.getenv('BOT_USERNAME', 'ㅇㅇ'),                  # 사용자 이름
    'password': os.getenv('BOT_PASSWORD', '12345'),                # 비밀번호 (보안상의 이유로 암호화 추천)
    'persona': os.getenv('BOT_PERSONA', "무뚝뚝한 성격의 마음은 따뜻한 여자 고등학생")  # 봇의 성격
}
