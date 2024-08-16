# dc_api_manager.py

import dc_api
import logging
from aiohttp import client_exceptions

class DcApiManager:
    def __init__(self, board_id, username, password):
        """
        DcApiManager를 초기화합니다.

        :param board_id: 게시판 ID
        :param username: 사용자 이름
        :param password: 비밀번호
        """
        self.board_id = board_id
        self.username = username
        self.password = password
        self.api = dc_api.API()  # API 세션 초기화

    async def start(self):
        """
        인스턴스를 시작합니다. 현재는 호환성을 위해 유지하고 있습니다.

        :return: 현재 인스턴스(self)
        """
        return self

    async def close(self):
        """
        API 세션을 명시적으로 종료합니다.
        """
        await self.api.close()

    async def write_document(self, title, content):
        """
        새로운 문서를 작성합니다.

        :param title: 문서 제목
        :param content: 문서 내용
        :return: 문서 ID, 실패 시 None
        """
        try:
            doc_id = await self.api.write_document(
                board_id=self.board_id,
                title=title,
                contents=content,
                name=self.username,
                password=self.password,
            )
            logging.info(f"문서 작성 성공 (ID: {doc_id}, 제목: {title})")
            return doc_id
        except client_exceptions.ContentTypeError as e:
            logging.error(f"문서 작성 실패 - 콘텐츠 유형 오류: {e}")
        except Exception as e:
            logging.error(f"문서 작성 실패: {e}")
        return None

    async def write_comment(self, document_id, comment_content):
        """
        문서에 댓글을 작성합니다.

        :param document_id: 문서 ID
        :param comment_content: 댓글 내용
        :return: 댓글 ID, 실패 시 None
        """
        try:
            comm_id = await self.api.write_comment(
                board_id=self.board_id,
                document_id=document_id,
                name=self.username,
                password=self.password,
                contents=comment_content,
            )
            logging.info(f"댓글 작성 성공 (ID: {comm_id}, 내용: {comment_content})")
            return comm_id
        except client_exceptions.ContentTypeError as e:
            logging.error(f"댓글 작성 실패 - 콘텐츠 유형 오류: {e}")
        except Exception as e:
            logging.error(f"댓글 작성 실패: {e}")
        return None

    async def get_trending_topics(self, num_articles):
        """
        최신 트렌딩 주제를 가져옵니다.

        :param num_articles: 가져올 기사 수
        :return: 기사 리스트, 실패 시 빈 리스트
        """
        try:
            articles = [article async for article in self.api.board(board_id=self.board_id, num=num_articles)]
            return articles
        except client_exceptions.ContentTypeError as e:
            logging.error(f"트렌딩 주제 가져오기 실패 - 콘텐츠 유형 오류: {e}")
        except Exception as e:
            logging.error(f"트렌딩 주제 가져오기 실패: {e}")
        return []
