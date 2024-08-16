import asyncio
import logging
import time
from config import API_KEYS, MODEL_NAME, GENERATION_CONFIG, DEFAULT_BOT_SETTINGS
from database import DatabaseManager
from bot import DcinsideBot
from gpt_api_manager import GptApiManager
from dc_api_manager import DcApiManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run_gallery_bot(api_key, bot_settings):
    """
    갤러리 봇을 실행합니다.

    :param api_key: API 키
    :param bot_settings: 봇 설정
    """
    bot_settings.update({'api_key': api_key})

    dc_api_manager = DcApiManager(
        board_id=bot_settings['board_id'],
        username=bot_settings['username'],
        password=bot_settings['password']
    )
    await dc_api_manager.start()

    db_managers = {
        'crawling': DatabaseManager(f"data/{bot_settings['board_id']}_crawling.db", "crawling"),
        'data': DatabaseManager(f"data/{bot_settings['board_id']}_data.db", "data"),
        'memory': DatabaseManager(f"data/{bot_settings['board_id']}_memory.db", "memory"),
    }

    try:
        await asyncio.gather(*[db_manager.connect() for db_manager in db_managers.values()])

        for db_manager in db_managers.values():
            if db_manager.conn is None:
                logging.error(f"{db_manager.db_type} 데이터베이스에 연결할 수 없습니다.")
                return

        gpt_api_manager = GptApiManager(api_key=api_key, model_name=MODEL_NAME, generation_config=GENERATION_CONFIG)

        bot = DcinsideBot(
            api_manager=dc_api_manager.api,
            db_managers=db_managers,
            gpt_api_manager=gpt_api_manager,
            persona=bot_settings['persona'],
            settings=bot_settings
        )

        await bot.get_trending_topics()
        await bot.record_gallery_information()

        start_time = time.time()

        while True:
            await asyncio.sleep(bot.settings['comment_interval'])
            trending_topics = await bot.get_trending_topics()
            memory_data = await bot.memory_db.load_memory(bot.settings['board_id']) if bot.settings.get('load_memory_enabled', True) else ""

            await bot.write_article(trending_topics, memory_data)

            if bot.settings.get('use_time_limit', False) and (time.time() - start_time) > bot.settings['max_run_time']:
                break

    except Exception as e:
        logging.error(f"봇 실행 중 오류 발생: {e}")

    finally:
        await asyncio.gather(*[db_manager.close() for db_manager in db_managers.values()])
        await dc_api_manager.close()

async def main():
    """
    메인 실행 함수
    """
    current_api_key_index = 0
    bot_settings_c1 = DEFAULT_BOT_SETTINGS.copy()
    bot_settings_c1.update({'board_id': 'comic_new4'})

    while True:
        current_api_key = API_KEYS[current_api_key_index]
        await run_gallery_bot(current_api_key, bot_settings_c1)
        await asyncio.sleep(900)  # 15분 대기
        current_api_key_index = (current_api_key_index + 1) % len(API_KEYS)

if __name__ == "__main__":
    asyncio.run(main())
