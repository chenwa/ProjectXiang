import os
import httpx
from dotenv import load_dotenv
from utils.logger import setup_logging
import logging

setup_logging()
logger = logging.getLogger('openai_api')

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set. Please define it in your .env file.")

async def query_ai(prompt: str, text: str, temperature: float, max_tokens: int):
    logger.info(f"Receiving prompt: {prompt} and text: {text}, temperature: {temperature}, max_tokens: {max_tokens}")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Assistant is a helpful AI."},
            {"role": "user", "content": f"{prompt} based on the following text: {text}"}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens  # token for no user (no login), regular user and premium user can adjust this
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            ai_content = result["choices"][0]["message"]["content"].strip()
            logger.info(f"Response from AI: {ai_content}")
            return {"response": ai_content}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {"error": str(e)}
