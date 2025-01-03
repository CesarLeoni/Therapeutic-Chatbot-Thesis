from openai import OpenAI
import os
from dotenv import load_dotenv
from conf.logger import get_logger

logger = get_logger(__name__)

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def fetch_response(prompt: str) -> str:
    try:
        logger.info(f"Fetching response for prompt: {prompt}")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Ești un psiholog multilingv..."},
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini-2024-07-18",
        )
        response = chat_completion.choices[0].message.content.strip()
        logger.debug(f"Received response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error fetching response: {e}", exc_info=True)
        return f"Error: {e}"
