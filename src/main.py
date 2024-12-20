from dotenv import load_dotenv
import os
import integration.telegram
from conf.logger import get_logger


import psycopg2
from psycopg2 import sql

import psycopg2
from psycopg2 import sql

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="MyChatbotDB1.0",
            user="cesar",
            password="ParolaBDLicenta2025",
            host="db",       # The service name from docker-compose.yml
            port="5432"
        )
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")




logger = get_logger(__name__)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

if __name__ == '__main__':
    conn = connect_to_db()
    logger.info("Starting main application")
    try:
        integration.telegram.main()
    except Exception as e:
        logger.critical(f"Critical error in main: {e}", exc_info=True)

    if conn:
        conn.close()