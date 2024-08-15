import asyncio
import logging
from bot import DcinsideBot
from config import BOARD_ID, USERNAME, PASSWORD, PERSONA, COMMENT_INTERVAL, \
    CRAWL_ARTICLE_COUNT, COMMENT_TARGET_COUNT, WRITE_COMMENT_ENABLED, \
    USE_TIME_LIMIT

async def main():
    """Function to run each gallery bot."""
    logging.info("Starting gallery bot")
    bot = DcinsideBot(
        board_id=BOARD_ID,
        username=USERNAME,
        password=PASSWORD,
        persona=PERSONA,
        comment_interval=COMMENT_INTERVAL,
        crawl_article_count=CRAWL_ARTICLE_COUNT,
        comment_target_count=COMMENT_TARGET_COUNT,
        write_comment_enabled=WRITE_COMMENT_ENABLED
    )
    await bot.run_comment_loop(USE_TIME_LIMIT)

if __name__ == "__main__":
    asyncio.run(main())
