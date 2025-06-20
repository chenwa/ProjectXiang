from pydantic import BaseModel

class OpenAiDTO(BaseModel):
    prompt: str = "Write a summary"  # Default prompt for the AI
    text: str = "Keywords of your thoughts"  # Text to be processed by the AI
    temperature: float = 0.7  # Default temperature for the response
    max_tokens: int = 1000  # Default max tokens for the response

