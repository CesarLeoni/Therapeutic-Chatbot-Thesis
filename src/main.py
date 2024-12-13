from dotenv import load_dotenv
import os
import integration.telegram
from conf.logger import get_logger


import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",  # This should match the password set in Docker Compose
    host="db",  # This refers to the service name in Docker Compose
    port="5432"
)



logger = get_logger(__name__)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

if __name__ == '__main__':
    logger.info("Starting main application")
    try:
        integration.telegram.main()
    except Exception as e:
        logger.critical(f"Critical error in main: {e}", exc_info=True)
