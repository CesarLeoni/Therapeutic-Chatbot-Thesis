from dotenv import load_dotenv
import os
import integration.telegram

import warnings
#
# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")


# Load environment variables from the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

if __name__ == '__main__':
    integration.telegram.main()