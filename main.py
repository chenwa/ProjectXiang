from fastapi import FastAPI
import logging
from utils.logger import setup_logging 
from models.user_model import UserModel
from models.address_model import AddressModel
from manage_user import (
    add_user, 
    add_user_address,
    authenticate_user_password,
    get_user_by_id, 
    delete_user_by_email,
    search_users_by_name,
    update_user_name_by_email
)

setup_logging()
logger = logging.getLogger('my_module')

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("/ reached")
    logger.debug("hello")
    logger.error("err")
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info(f"/items/{item_id}")
    return {"item_id": item_id, "q": q}

@app.get("/users/{user_id}")
def read_user(id: int):
    logger.info(f"id: {id}")
    return {"user": get_user_by_id(id)}

@app.post("/users_create/")
def create_user(user: UserModel, address: AddressModel):
    logger.info(f"adding user: {user.first_name}, {user.email}")
    return {"user": add_user(user, address)}

@app.delete("/user_delete/{email}")
def delete_user(email: str):
    logger.info(f"deleting user with email: {email}")
    return {"success": delete_user_by_email(email)}

@app.post("/user_update_name/{email}/{new_name}")
def update_user_name(email: str, new_name: str):
    logger.info(f"updating username of {email} to {new_name}")
    return {"success": update_user_name_by_email(email, new_name)} 

@app.get("/search_users_by_name/{query}")
def find_users_by_name(query: str):
    logger.info(f"finding users with names that contain {query}")
    return {"users": search_users_by_name(query)} 

@app.get("/users/{email}/{password}")
def authenticate_user(email: str, password: str):
    logger.info(f"Validating user: {email}")
    return {"success": authenticate_user_password(email, password)}

@app.post("/add_user_address/")
def add_user_address_endpoint(address: AddressModel):
    logger.info(f"adding address of {address.user_id}")
    return {"message": add_user_address(address.user_id, address.street,
                                        address.city, address.state, 
                                        address.zip_code, address.country)}




