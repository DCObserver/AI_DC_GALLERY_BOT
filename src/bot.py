import logging
import re
import time
from collections import Counter
from utils import handle_exceptions, sanitize_text

class DcinsideBot:
    def __init__(self, api_manager, db_managers, gpt_api_manager, persona, settings):
        """
        DcinsideBot 클래스를 초기화합니다.

        :param api_manager: DCInside API 관리 객체
        :param db_managers: 데이터베이스 관리 객체들
        :param gpt_api_manager: GPT API 관리 객체
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
        self.write_article_enabled = settings.get('write_article_enabled', True)
        self.write_comment_enabled = settings.get('write_comment_enabled', True)
        self.board_id = settings['board_id']
        self.username = settings['username']
        self.password = settings['password']

    @handle_exceptions
    async def get_trending_topics(self):
        """
        최신 트렌딩 토픽을 가져옵니다.

        :return: 최신 토픽의 카운터 객체
        """
        articles = [article async for article in self.api_manager.api.board(
            board_id=self.board_id,
            num=self.settings['crawl_article_count']
        )]
        title_list = [article.title for article in articles]
        return Counter(title_list)

    @handle_exceptions
    async def record_gallery_information(self):
        """
        갤러리 정보를 메모리에 기록합니다.
        """
        if not self.settings.get('record_memory_enabled', True):
            return

        articles = [article async for article in self.api_manager.api.board(
            board_id=self.board_id,
            num=self.settings['crawl_article_count']
        )]
        memory_content = await self.generate_memory_from_crawling(articles)
        await self.memory_db.save_data(
            board_id=self.board_id,
            memory_content=memory_content
        )

    async def generate_memory_from_crawling(self, articles):
        """
        크롤링한 정보를 바탕으로 메모리 콘텐츠를 생성합니다.

        :param articles: 크롤링한 기사들
        :return: 생성된 메모리 콘텐츠
        """
        crawling_info = "\n".join([f"제목: {article.title}, 저자: {article.author}" for article in articles])
        prompt = f"""
        {self.persona}

        디시인사이드 갤러리에서 크롤링한 정보를 바탕으로, {self.persona} 페르소나에 맞춰서 메모리를 작성해줘.

        크롤링 정보:
        {crawling_info}
        """
        content = await self.gpt_api_manager.generate_content(prompt)
        return sanitize_text(content)

    async def write_article(self, trending_topics, memory_data=None):
        """
        언어 모델을 이용하여 글 제목과 내용을 생성하고 게시합니다.

        :param trending_topics: 최신 트렌딩 토픽
        :param memory_data: 갤러리의 최근 정보
        :return: 작성된 글의 문서 ID와 제목
        """
        if not self.write_article_enabled:
            return None

        top_trending_topics = [topic[0] for topic in trending_topics.most_common(3)]

        prompt = f"""
        {self.persona} 페르소나 규칙 꼭 지키기.

        {self.board_id} 갤러리에 어울리는 흥미로운 글 제목을 짓고, 최근 유행하는 토픽을 참고하여 글을 쓰되, 페르소나에 맞춰서 작성해줘.

        최근 {self.board_id} 갤러리에서 유행하는 토픽은 다음과 같습니다:
        {trending_topics}

        특히 다음 토픽들을 중심으로 글 내용을 구성해줘:
        {', '.join(top_trending_topics)}

        글 제목은 유행 토픽을 참고하여 새롭게 지어줘.
        제목은 {self.persona}에 맞춰서 작성해줘.

        갤러리의 최근 정보를 참고하여 글 내용을 더욱 풍성하게 만들어줘:
        {memory_data}
        글은 최대 300자로 작성해줘.
        """
        while True:
            try:
                content = await self.gpt_api_manager.generate_content(prompt)
                
                if not content:
                    raise ValueError("생성된 콘텐츠가 비어있습니다.")
                
                # 제목과 내용 분리
                title, content = content.split('\n', 1)
                title = sanitize_text(title).replace("##", "")
                content = sanitize_text(content)

                doc_id = await self.api_manager.write_document(
                    title=title,
                    content=content
                )
                # 성공 메시지 삭제

                # 데이터 저장
                await self.data_db.save_data(
                    content_type="article",
                    doc_id=doc_id,
                    content=title,
                    board_id=self.board_id
                )

                return doc_id, title
            except Exception as e:
                logging.error(f"글 작성 실패: {e}")
                await asyncio.sleep(self.settings['article_interval'])

    async def write_comment(self, document_id, article_title):
        """
        언어 모델을 이용하여 댓글 내용을 생성하고 게시합니다.

        :param document_id: 문서 ID
        :param article_title: 글 제목
        :return: 댓글 작성 성공 여부
        """
        if not self.write_comment_enabled:
            return None

        prompt = f"""
        {self.persona}

        다음 글에 대한 댓글을 페르소나에 충실하게 작성해.

        댓글 작성에 제목 내용 참고: {article_title}

        댓글은 페르소나에 충실하게 작성해. 댓글은 최대 120자.
        """
        while True:
            try:
                content = await self.gpt_api_manager.generate_content(prompt)

                if not content:
                    raise ValueError("생성된 콘텐츠가 비어있습니다.")
                
                comment_content = sanitize_text(content).strip()

                comm_id = await self.api_manager.write_comment(
                    document_id=document_id,
                    content=comment_content
                )
                first_sentence = comment_content.split('\n')[0]
                # 성공 메시지 삭제

                # 데이터 저장
                await self.data_db.save_data(
                    content_type="comment",
                    doc_id=document_id,
                    content=first_sentence,
                    board_id=self.board_id
                )

                return True
            except Exception as e:
                logging.error(f"댓글 작성 실패: {e}")
                await asyncio.sleep(5)
