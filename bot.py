import asyncio
import random
import logging
from time import time
from config import BOARD_ID, USERNAME, PASSWORD, PERSONA, COMMENT_INTERVAL, \
    CRAWL_ARTICLE_COUNT, COMMENT_TARGET_COUNT, WRITE_COMMENT_ENABLED, \
    USE_TIME_LIMIT, MAX_RUN_TIME, model, generation_config
import dc_api
from filter import clean_comment

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DcinsideBot:
    def __init__(self, board_id, username, password, persona, comment_interval, crawl_article_count,
                 comment_target_count, write_comment_enabled):
        self.board_id = board_id
        self.username = username
        self.password = password
        self.persona = persona
        self.comment_interval = comment_interval
        self.crawl_article_count = crawl_article_count
        self.comment_target_count = comment_target_count
        self.write_comment_enabled = write_comment_enabled

    async def write_comment(self, document_id, article_title):
        if not self.write_comment_enabled:
            return None

        prompt = self.create_prompt(article_title)
        try:
            comment_content = await self.generate_comment(prompt)
            cleaned_comment = clean_comment(comment_content)
            comm_id = await self.post_comment(document_id, cleaned_comment)
            logging.info(f"Comment posted! (ID: {comm_id}) (Content: {cleaned_comment.split('\n')[0]}) Title: {article_title}")
            return True
        except Exception as e:
            logging.error(f"Failed to post comment: {e}")
            return False

    def create_prompt(self, article_title):
        return f"""
        Persona:
        {self.persona}

        Input: {article_title}

        Write a response fitting the persona within 100 characters.
        """

    async def generate_comment(self, prompt):
        response = model.generate_content(
            [prompt],
            safety_settings={
                'HATE_SPEECH': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'DANGEROUS_CONTENT': 'BLOCK_NONE'
            },
            generation_config=generation_config
        )
        return response.text.strip()

    async def post_comment(self, document_id, comment_content):
        async with dc_api.API() as api:
            return await api.write_comment(
                board_id=self.board_id,
                document_id=document_id,
                name=self.username,
                password=self.password,
                contents=comment_content,
            )

    async def run_comment_loop(self, use_time_limit):
        start_time = time()
        while (use_time_limit and time() - start_time < MAX_RUN_TIME) or not use_time_limit:
            await asyncio.sleep(self.comment_interval)
            latest_articles = await self.fetch_latest_articles()
            if latest_articles:
                selected_article = random.choice(latest_articles)
                comment_success = await self.write_comment(selected_article.id, selected_article.title)
                while not comment_success:
                    await asyncio.sleep(5)
                    selected_article = random.choice(latest_articles)
                    comment_success = await self.write_comment(selected_article.id, selected_article.title)

    async def fetch_latest_articles(self):
        async with dc_api.API() as api:
            return [article async for article in api.board(board_id=self.board_id, num=self.comment_target_count)]
