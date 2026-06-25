import pymysql
from pymysql.cursors import DictCursor

from src.config import settings
from src.utils.logger import logger


class MySQLHelper:
    """Small reusable MySQL helper used by ETL, analysis, and Flask API."""

    def __init__(self, database: str | None = None):
        self.host = settings.MYSQL_HOST
        self.port = settings.MYSQL_PORT
        self.user = settings.MYSQL_USER
        self.password = settings.MYSQL_PASSWORD
        self.database = database if database is not None else settings.MYSQL_DATABASE

    def get_connection(self):
        kwargs = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "charset": "utf8mb4",
            "cursorclass": DictCursor,
            "autocommit": False,
        }
        if self.database:
            kwargs["database"] = self.database
        return pymysql.connect(**kwargs)

    def execute(self, sql: str, params=None) -> int:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                affected = cursor.execute(sql, params)
            connection.commit()
            return affected
        except Exception:
            connection.rollback()
            logger.exception("MySQL execute failed")
            raise
        finally:
            connection.close()

    def execute_many(self, sql: str, data: list[tuple]) -> int:
        if not data:
            return 0
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                affected = cursor.executemany(sql, data)
            connection.commit()
            return affected
        except Exception:
            connection.rollback()
            logger.exception("MySQL execute_many failed")
            raise
        finally:
            connection.close()

    def fetch_all(self, sql: str, params=None) -> list[dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception:
            logger.exception("MySQL fetch_all failed")
            raise
        finally:
            connection.close()

    def fetch_one(self, sql: str, params=None) -> dict | None:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except Exception:
            logger.exception("MySQL fetch_one failed")
            raise
        finally:
            connection.close()
