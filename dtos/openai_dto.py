from pydantic import BaseModel

class OpenAiDTO(BaseModel):
    model: str = "gpt-4o"  # Default model for OpenAI API    
    prompt: str = "Write a report based on the following input"  # Default prompt for the AI
    text: str = "Keywords of your thoughts"  # Text to be processed by the AI
    temperature: float = 0.3  # Default temperature for the response
    max_tokens: int = 1000  # Default max tokens for the response

