from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

#model : gpt-4o-mini-2024-07-18

# Load your OpenAI API key from the environment variable
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

async def fetch_response(prompt: str) -> str:
    """
    Sends the given prompt to OpenAI's GPT model and fetches a response.
    :param prompt: The user's input message.
    :return: The generated response from the OpenAI API.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are acting like a good therapist. Your name is PsychoBot and you listen carefully."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            model="gpt-4o-mini-2024-07-18"
            #temperature=0.7,  # Adjust for creativity
        )
        # Access the response content properly
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"