from pydantic import BaseModel

class UserDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
