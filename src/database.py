# database.py - Database management for different data types

import aiosqlite
import os
import logging

class DatabaseManager:
    def __init__(self, db_file, db_type):
        self.db_file = os.path.join(".", db_file)
        self.db_type = db_type
        self.conn = None  # 초기화에서 연결 객체는 None으로 설정

    async def connect(self):
        try:
            self.conn = await aiosqlite.connect(self.db_file)
            await self.create_tables()
            logging.info(f"Connected to database {self.db_file} successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            self.conn = None

    async def create_tables(self):
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
            logging.info("Tables created successfully.")
        except Exception as e:
            logging.error(f"Failed to create tables: {e}")

    async def save_data(self, **kwargs):
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
            logging.info(f"Data saved successfully: {kwargs}")
        except Exception as e:
            logging.error(f"Failed to save data: {e}")

    async def load_memory(self, board_id):
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
                logging.info("Memory loaded successfully")
                return row[0]
            else:
                logging.info("No memory found")
                return ""
        except Exception as e:
            logging.error(f"Failed to load memory: {e}")
            return ""

    async def close(self):
        if self.conn:
            try:
                await self.conn.close()
                logging.info("Database connection closed successfully.")
            except Exception as e:
                logging.error(f"Failed to close the database connection: {e}")
        else:
            logging.warning("No database connection to close.")
