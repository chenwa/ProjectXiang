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
    """
    Root endpoint that returns a welcome message.
    """
    logger.info("/ reached")
    logger.debug("hello")
    logger.error("err")
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
    Endpoint to retrieve an item by its ID.

    Parameters:
        item_id (int): The ID of the item.
        q (str, optional): An optional query parameter.

    Returns:
        dict: The item ID and query parameter.
    """
    logger.info(f"/items/{item_id}")
    return {"item_id": item_id, "q": q}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    """
    Endpoint to retrieve a user by their ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict: The user object.
    """
    logger.info(f"Retrieving user with ID: {user_id}")
    return {"user": get_user_by_id(user_id)}


@app.post("/users_create/")
def create_user(user: UserModel, address: AddressModel):
    """
    Endpoint to create a new user and their address.

    Parameters:
        user (UserModel): The user model containing user details.
        address (AddressModel): The address model containing address details.

    Returns:
        dict: The created user object.
    """
    logger.info(f"Adding user: {user.first_name}, {user.email}")
    return {"user": add_user(user, address)}


@app.delete("/user_delete/{email}")
def delete_user(email: str):
    """
    Endpoint to delete a user by their email.

    Parameters:
        email (str): The email of the user to delete.

    Returns:
        dict: Success status of the deletion.
    """
    logger.info(f"Deleting user with email: {email}")
    return {"success": delete_user_by_email(email)}


@app.post("/user_update_name/{email}/{new_name}")
def update_user_name(email: str, new_name: str):
    """
    Endpoint to update a user's name by their email.

    Parameters:
        email (str): The email of the user.
        new_name (str): The new name to assign.

    Returns:
        dict: Success status of the update.
    """
    logger.info(f"Updating username of {email} to {new_name}")
    return {"success": update_user_name_by_email(email, new_name)}


@app.get("/search_users_by_name/{query}")
def find_users_by_name(query: str):
    """
    Endpoint to search for users by a name query.

    Parameters:
        query (str): The substring to search for in user names.

    Returns:
        dict: A list of matching users.
    """
    logger.info(f"Finding users with names that contain: {query}")
    return {"users": search_users_by_name(query)}


@app.get("/users/{email}/{password}")
def authenticate_user(email: str, password: str):
    """
    Endpoint to authenticate a user by their email and password.

    Parameters:
        email (str): The email of the user.
        password (str): The plaintext password of the user.

    Returns:
        dict: Success status of the authentication.
    """
    logger.info(f"Validating user: {email}")
    return {"success": authenticate_user_password(email, password)}


@app.post("/add_user_address/")
def add_user_address_endpoint(address: AddressModel):
    """
    Endpoint to add an address for a user.

    Parameters:
        address (AddressModel): The address model containing address details.

    Returns:
        dict: Success message and address details.
    """
    logger.info(f"Adding address for user ID: {address.user_id}")
    return {
        "message": add_user_address(
            address.user_id,
            address.street,
            address.city,
            address.state,
            address.zip_code,
            address.country
        )
    }




