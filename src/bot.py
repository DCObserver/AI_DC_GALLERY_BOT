import logging
from collections import Counter
from aiohttp import client_exceptions

class DcinsideBot:
    def __init__(self, api_manager, db_managers, gpt_api_manager, persona, settings):
        """
        DcinsideBot 인스턴스를 초기화합니다.

        :param api_manager: DcApiManager 인스턴스
        :param db_managers: 데이터베이스 관리자 딕셔너리
        :param gpt_api_manager: GptApiManager 인스턴스
        :param persona: 봇의 페르소나
        :param settings: 봇 설정
        """
        self.api_manager = api_manager
        self.crawling_db = db_managers['crawling']
        self.data_db = db_managers['data']
        self.memory_db = db_managers['memory']
        self.gpt_api_manager = gpt_api_manager
        self.persona = persona
        self.settings = settings

    async def get_trending_topics(self):
        """
        유행하는 토픽을 가져옵니다.

        :return: 유행하는 토픽의 Counter 객체
        """
        try:
            articles = [article async for article in self.api_manager.board(
                board_id=self.settings['board_id'],
                num=self.settings['crawl_article_count']
            )]
            title_list = [article.title for article in articles]
            return Counter(title_list)
        except client_exceptions.ContentTypeError as e:
            logging.error(f"유행하는 토픽 가져오기 실패 - 콘텐츠 유형 오류: {e}")
        except Exception as e:
            logging.error(f"유행하는 토픽 가져오기 실패: {e}")
        return Counter()

    async def record_gallery_information(self):
        """
        갤러리 정보를 기록합니다.
        """
        if not self.settings.get('record_memory_enabled', True):
            return

        try:
            articles = [article async for article in self.api_manager.board(
                board_id=self.settings['board_id'],
                num=self.settings['crawl_article_count']
            )]
            memory_content = await self.generate_memory_from_crawling(articles)
            await self.memory_db.save_data(
                board_id=self.settings['board_id'],
                memory_content=memory_content
            )
        except client_exceptions.ContentTypeError as e:
            logging.error(f"갤러리 정보 기록 실패 - 콘텐츠 유형 오류: {e}")
        except Exception as e:
            logging.error(f"갤러리 정보 기록 실패: {e}")

    async def generate_memory_from_crawling(self, articles):
        """
        크롤링한 데이터를 기반으로 메모리를 생성합니다.

        :param articles: 크롤링한 기사 리스트
        :return: 생성된 메모리 콘텐츠
        """
        crawling_info = "\n".join([f"제목: {article.title}, 저자: {article.author}" for article in articles])
        prompt = f"""
        {self.persona}

        디시인사이드 갤러리에서 크롤링한 정보를 바탕으로, {self.persona} 페르소나에 맞춰서 메모리를 작성해줘.

        크롤링 정보:
        {crawling_info}
        """
        return await self.gpt_api_manager.generate_content(prompt)

    async def write_article(self, trending_topics, memory_data):
        """
        유행하는 토픽과 메모리 데이터를 바탕으로 게시글을 작성합니다.

        :param trending_topics: 유행하는 토픽
        :param memory_data: 메모리 데이터
        """
        prompt = f"""
        {self.persona} 페르소나 규칙 꼭 지키기.

        {self.settings['board_id']} 갤러리에 어울리는 흥미로운 글 제목을 짓고, 최근 유행하는 토픽을 참고하여 글을 쓰되, 페르소나에 맞춰서.

        최근 {self.settings['board_id']} 갤러리에서 유행하는 토픽은 다음과 같습니다:
        {trending_topics}

        글 제목은 {self.persona}에 맞춰서.

        갤러리의 최근 정보를 참고하여 글 내용을 더욱 풍성하게 만들어줘:
        {memory_data}
        글은 최대 700자로 작성해줘.
        """
        content = await self.gpt_api_manager.generate_content(prompt)
        if content:
            title, body = content.split('\n', 1)
            title = title.replace("##", "").strip()
            doc_id = await self.api_manager.write_document(title, body)
            
            if doc_id:
                logging.info(f"게시글 작성 성공 (ID: {doc_id})")
                await self.data_db.save_data(
                    content_type='article',
                    doc_id=doc_id,
                    content=title,
                    board_id=self.settings['board_id']
                )
            else:
                logging.error("게시글 작성 실패.")
