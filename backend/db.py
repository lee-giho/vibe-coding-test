import pymysql
from contextlib import contextmanager
from config import Config

class Database:
    """MySQL 데이터베이스 연결 관리"""
    
    @staticmethod
    def get_connection():
        """MySQL 연결 생성"""
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
    
    @staticmethod
    @contextmanager
    def get_cursor(commit=False):
        """
        컨텍스트 매니저로 커서 제공
        
        Args:
            commit (bool): True면 자동 커밋, False면 수동 처리
        """
        connection = None
        cursor = None
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            yield cursor
            if commit:
                connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @staticmethod
    def check_health():
        """데이터베이스 연결 상태 확인"""
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"DB Health Check Error: {e}")
            import traceback
            traceback.print_exc()
            return False
