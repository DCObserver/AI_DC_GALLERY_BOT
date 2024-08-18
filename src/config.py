import os
from dotenv import load_dotenv
from google.generativeai import GenerationConfig

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키를 불러오고, 쉼표로 구분된 값을 리스트로 변환
API_KEYS = os.getenv('API_KEYS')
API_KEYS = API_KEYS.split(',') if API_KEYS else None

# 모델 설정
MODEL_NAME = os.getenv('MODEL_NAME')
GENERATION_CONFIG = GenerationConfig(
    temperature=float(os.getenv('GEN_TEMPERATURE')),
    top_k=int(os.getenv('GEN_TOP_K')),
    max_output_tokens=int(os.getenv('GEN_MAX_OUTPUT_TOKENS'))
)

# 기본 봇 설정 (공통 설정)
DEFAULT_BOT_SETTINGS = {
    'max_run_time': int(os.getenv('BOT_MAX_RUN_TIME')),
    'article_interval': int(os.getenv('BOT_ARTICLE_INTERVAL')),
    'comment_interval': int(os.getenv('BOT_COMMENT_INTERVAL')),
    'crawl_article_count': int(os.getenv('BOT_CRAWL_ARTICLE_COUNT')),
    'comment_target_count': int(os.getenv('BOT_COMMENT_TARGET_COUNT')),
    'write_article_enabled': os.getenv('BOT_WRITE_ARTICLE_ENABLED') == 'True',
    'write_comment_enabled': os.getenv('BOT_WRITE_COMMENT_ENABLED') == 'True',
    'record_memory_enabled': os.getenv('BOT_RECORD_MEMORY_ENABLED') == 'True',
    'record_data_enabled': os.getenv('BOT_RECORD_DATA_ENABLED') == 'True',
    'use_time_limit': os.getenv('BOT_USE_TIME_LIMIT') == 'True',
    'load_memory_enabled': os.getenv('BOT_LOAD_MEMORY_ENABLED') == 'True',
    'load_data_enabled': os.getenv('BOT_LOAD_DATA_ENABLED') == 'True',
    'gallery_record_interval': int(os.getenv('BOT_GALLERY_RECORD_INTERVAL')),
    'username': os.getenv('BOT_USERNAME'),
    'password': os.getenv('BOT_PASSWORD'),
    'persona': os.getenv('BOT_PERSONA')
}
