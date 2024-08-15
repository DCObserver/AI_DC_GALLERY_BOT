import os
import google.generativeai as genai

# Configuration constants
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Use environment variable for API key
BOARD_ID = 'your_board_id'
USERNAME = 'your_username'
PASSWORD = 'your_password'
PERSONA = """
your_persona
"""
MAX_RUN_TIME = 1800  # Maximum run time (seconds)
COMMENT_INTERVAL = 30  # Comment interval (seconds)
CRAWL_ARTICLE_COUNT = 20  # Number of articles to crawl
COMMENT_TARGET_COUNT = 15  # Number of articles to target for comments
WRITE_COMMENT_ENABLED = True  # Enable comment writing
USE_TIME_LIMIT = False  # Use time limit

# Google API setup
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
generation_config = genai.GenerationConfig(
    temperature=0.6,
    top_k=1,
    max_output_tokens=750
)
