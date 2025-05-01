from pydantic import BaseModel

class AddressModel(BaseModel):
    user_id: int
    street: str
    city: str
    state: str
    zip_code: str
    country: str

