import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask 애플리케이션 설정"""
    
    # MySQL 설정
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'poll_db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'poll_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'poll_password_2025')
    
    # Flask 설정
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    TIMEZONE = 'Asia/Seoul'
