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
        logging.info("API session closed.")

    async def write_document(self, title, content, is_minor=False):
        """
        새로운 문서를 작성합니다.

        :param title: 문서 제목
        :param content: 문서 내용
        :param is_minor: 마이너 갤러리 여부
        :return: 문서 ID, 실패 시 None
        """
        logging.info(f"Attempting to write document with title: {title}")
        try:
            doc_id = await self.api.write_document(
                board_id=self.board_id,
                title=title,
                contents=content,
                name=self.username,
                password=self.password,
                is_minor=is_minor
            )
            logging.info(f"Document written with ID: {doc_id}")
            return doc_id
        except client_exceptions.ContentTypeError as e:
            logging.error(f"Document write failed - ContentTypeError: {e}")
        except Exception as e:
            logging.error(f"Document write failed: {e}")
        return None

    async def write_comment(self, doc_id, content):
        """
        문서에 댓글을 작성합니다.

        :param doc_id: 문서 ID
        :param content: 댓글 내용
        :return: 댓글 ID, 실패 시 None
        """
        logging.info(f"Attempting to write comment to document ID: {doc_id}")
        try:
            comment_id = await self.api.write_comment(
                board_id=self.board_id,
                doc_id=doc_id,
                name=self.username,
                password=self.password,
                contents=content
            )
            logging.info(f"Comment written with ID: {comment_id}")
            return comment_id
        except client_exceptions.ContentTypeError as e:
            logging.error(f"Comment write failed - ContentTypeError: {e}")
        except Exception as e:
            logging.error(f"Comment write failed: {e}")
        return None
