from fastapi import FastAPI
import logging
from utils.logger import setup_logging 
from manage_user import (
    add_user, 
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

@app.post("/users_create/{name}/{email}/{password}")
def create_user(name: str, email: str, password):
    logger.info(f"adding user: {name}, {email}")
    return {"user": add_user(name, email, password)}

@app.delete("/user_delete/{email}")
def delete_user(email: str):
    logger.info(f"deleting user with email: {email}")
    return {"success": delete_user_by_email(email)}

@app.post("/user_update/{email}/{new_name}")
def update_user(email: str, new_name: str):
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



