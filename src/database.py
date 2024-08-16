import aiosqlite
import os
import logging

class DatabaseManager:
    def __init__(self, db_file, db_type):
        """
        데이터베이스 관리자를 초기화합니다.

        :param db_file: 데이터베이스 파일 이름
        :param db_type: 데이터베이스 유형 (crawling, data, memory)
        """
        self.db_file = os.path.join(".", db_file)  # 현재 디렉토리에 데이터베이스 파일 경로 설정
        self.db_type = db_type
        self.conn = None

    async def connect(self):
        """
        데이터베이스에 비동기적으로 연결하고 테이블을 생성합니다.
        """
        try:
            # 데이터베이스 디렉토리 생성
            db_dir = os.path.dirname(self.db_file)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)

            # 데이터베이스 파일이 없으면 생성
            if not os.path.exists(self.db_file):
                open(self.db_file, 'a').close()  # 빈 파일을 생성합니다.

            # 데이터베이스에 연결
            self.conn = await aiosqlite.connect(self.db_file)
            await self.create_tables()
            # 성공 메시지 삭제
            # logging.info(f"Connected to database {self.db_file} successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            self.conn = None

    async def create_tables(self):
        """
        데이터베이스 유형에 따라 필요한 테이블을 생성합니다.
        """
        if self.conn is None:
            logging.error("Connection to the database is not established.")
            return

        try:
            cursor = await self.conn.cursor()
            if self.db_type == "crawling":
                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS crawled_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        board_id TEXT,
                        article_title TEXT,
                        author_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            elif self.db_type == "data":
                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS generated_content (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content_type TEXT,  -- 'article' 또는 'comment'
                        doc_id TEXT,  -- 글 ID (댓글의 경우, 관련 글 ID)
                        content TEXT,  -- 글/댓글 내용
                        board_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            elif self.db_type == "memory":
                await cursor.execute('''
                    CREATE TABLE IF NOT EXISTS gallery_memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        board_id TEXT,
                        memory_content TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            await self.conn.commit()
            # 성공 메시지 삭제
            # logging.info("Tables created successfully.")
        except Exception as e:
            logging.error(f"Failed to create tables: {e}")

    async def save_data(self, **kwargs):
        """
        데이터베이스에 데이터를 저장합니다.

        :param kwargs: 데이터베이스에 저장할 데이터 (키워드 인자)
        """
        if self.conn is None:
            logging.error("Connection to the database is not established.")
            return

        try:
            cursor = await self.conn.cursor()
            if self.db_type == "crawling":
                await cursor.execute('''
                    INSERT INTO crawled_data (board_id, article_title, author_id)
                    VALUES (:board_id, :article_title, :author_id)
                ''', kwargs)
            elif self.db_type == "data":
                await cursor.execute('''
                    INSERT INTO generated_content (content_type, doc_id, content, board_id)
                    VALUES (:content_type, :doc_id, :content, :board_id)
                ''', kwargs)
            elif self.db_type == "memory":
                await cursor.execute('''
                    INSERT INTO gallery_memory (board_id, memory_content)
                    VALUES (:board_id, :memory_content)
                ''', kwargs)
            await self.conn.commit()
            # 성공 메시지 삭제
            # logging.info(f"Data saved successfully: {kwargs}")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")

    async def load_memory(self, board_id):
        """
        'memory' 데이터베이스에서 메모리를 로드합니다.

        :param board_id: 메모리를 로드할 게시판 ID
        :return: 로드된 메모리 내용
        """
        if self.conn is None:
            logging.error("Connection to the database is not established.")
            return ""

        if self.db_type != "memory":
            logging.warning("Memory data can only be loaded from the 'memory' database.")
            return ""

        try:
            cursor = await self.conn.cursor()
            await cursor.execute('''
                SELECT memory_content
                FROM gallery_memory
                WHERE board_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            ''', (board_id,))
            row = await cursor.fetchone()
            if row:
                # 성공 메시지 삭제
                # logging.info("Memory loaded successfully")
                return row[0]
            else:
                # 성공 메시지 삭제
                # logging.info("No memory found")
                return ""
        except Exception as e:
            logging.error(f"Failed to load memory: {e}")
            return ""

    async def close(self):
        """
        데이터베이스 연결을 닫습니다.
        """
        if self.conn:
            try:
                await self.conn.close()
                # 성공 메시지 삭제
                # logging.info("Database connection closed successfully.")
            except Exception as e:
                logging.error(f"Failed to close the database connection: {e}")
        else:
            logging.warning("No database connection to close.")
