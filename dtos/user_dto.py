from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    org: str
    password: str
