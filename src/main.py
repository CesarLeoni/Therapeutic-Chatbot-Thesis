from dotenv import load_dotenv
import os
import integration.telegram
from conf.logger import get_logger
import psycopg2
from psycopg2 import sql
import warnings

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

# Get the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Ensure DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")


def connect_to_db():
    try:
        # Connect using the DATABASE_URL
        conn = psycopg2.connect(DATABASE_URL)
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")


logger = get_logger(__name__)



warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

if __name__ == '__main__':
    conn = connect_to_db()
    logger.info("Starting main application")
    try:
        integration.telegram.main()
    except Exception as e:
        logger.critical(f"Critical error in main: {e}", exc_info=True)

    if conn:
        conn.close()
