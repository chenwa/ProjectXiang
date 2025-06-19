from fastapi import FastAPI, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import logging
from utils.logger import setup_logging
from utils.bulk_upload import router
from dtos.user_dto import UserDTO
from dtos.address_dto import AddressDTO
from manage_user import (
    add_user,
    add_user_address,
    authenticate_user_password,
    get_user_by_id,
    delete_user_by_email,
    search_users_by_email,
    update_user_name_by_email,
    return_user_by_email,
    get_user_id_by_email
)
from db.session_objects import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# Initialize the database schema
Base.metadata.create_all(bind=engine)

setup_logging()
logger = logging.getLogger('px')

# Secret key for session management
SECRET = "this_secret_needs_to_be_in_.env_file"
manager = LoginManager(SECRET, token_url="/login")

@manager.user_loader()
def load_user(email: str, org: str):
    """
    Load user from the database using their email and org.

    Parameters:
        email (str): The email of the user.
        org (str): The organization of the user.

    Returns:
        dict or None: The user object if found, otherwise None.
    """
    logger.info(f"Attempting to load user with email: {email} for {org}")

    user = return_user_by_email(email, org)
    if user:
        logger.info(f"User found: {user.email} in {org}")
        return user.email
    logger.warning(f"No user found for {org}")
    return None

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://main.d3eff9q6tcfn87.amplifyapp.com"  # Amplify frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), org: str = Form(...)):
    """
    Login endpoint to authenticate a user and return a session token.

    Parameters:
        email (str): The email of the user.
        org (str): The organization of the user.
        password (str): The plaintext password of the user.

    Returns:
        dict: A session token if authentication is successful.
    """
    email = data.username
    password = data.password

    logger.info(f"Validating user: {email} for organization: {org}")
    if not authenticate_user_password(email, password, org):
        raise InvalidCredentialsException

    # Create the token with the user's email as the subject
    access_token = manager.create_access_token(data={"sub": email})
    logger.info(f"Generated access_token for {email}: {access_token}")  # Log the access token
    
    return {"access_token": access_token, "token_type": "bearer"}

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

@app.post("/users_create")
def create_user(user: UserDTO):
    """
    Endpoint to create a new user.
    
    Parameters:
        user (UserDTO): The user model containing user details.
    
    Returns:
        dict: The created user object.
    """
    logger.info(f"Adding user: {user.first_name}, {user.email}")
    return {"user": add_user(user)}

@app.delete("/user_delete/{email}/{org}")
def delete_user(email: str, org: str):
    """
    Endpoint to delete a user by their email and organization.

    Parameters:
        email (str): The email of the user to delete.
        org (str): The organization of the user to delete.

    Returns:
        dict: Success status of the deletion.
    """
    logger.info(f"Deleting user with email: {email} for organization: {org}")
    return {"success": delete_user_by_email(email, org)}

@app.post("/user_update_name/{email}/{new_name}/{org}")
def update_user_name(email: str, new_name: str, org: str):
    """
    Endpoint to update a user's name by their email and organization.

    Parameters:
        email (str): The email of the user.
        org (str): The organization of the user.
        new_name (str): The new name to assign.

    Returns:
        dict: Success status of the update.
    """
    logger.info(f"Updating first_name of {email} for {org} to {new_name}")
    return {"success": update_user_name_by_email(email, new_name, org)}

@app.get("/search_users_by_name/{query}/{org}")
def find_users_by_email(query: str, org: str):
    """
    Endpoint to search for users by a email query.

    Parameters:
        query (str): The substring to search for in user email.
        org (str): The organization to filter users by.

    Returns:
        dict: A list of matching users.
    """
    logger.info(f"Finding users with emails that contain: {query} for organization: {org}")
    return {"users": search_users_by_email(query, org)}

@app.get("/users/{email}/{password}/{org}")
def authenticate_user(email: str, password: str, org: str):
    """
    Endpoint to authenticate a user by their email and password for organization.

    Parameters:
        email (str): The email of the user.
        org (str): The organization of the user.
        password (str): The plaintext password of the user.

    Returns:
        dict: Success status of the authentication.
    """
    logger.info(f"Validating user: {email} for organization: {org}")
    return {"success": authenticate_user_password(email, password, org)}

@app.post("/add_user_address")
def add_user_address_endpoint(
    address: AddressDTO,
    user=Depends(manager)
):
    """
    Endpoint to add an address for a user. Requires login.

    Parameters:
        address (AddressDTO): The address model containing address details.
        user: The authenticated user (populated by the access token).

    Returns:
        dict: Success message and address details.
    """
    logger.info(f"Authenticated user: {user}")  # Log the authenticated user

    # Get the user_id for the authenticated user
    user_id = get_user_id_by_email(user)
    # Always set the user_id from the token, not from the client
    address.user_id = user_id

    # Call add_user_address from manage_user.py to add the address
    result = add_user_address(
        address.user_id,
        address.street,
        address.city,
        address.state,
        address.zip_code,
        address.country
    )
    logger.info(f"add_user_address result: {result}")
    return {
        "message": "Address added successfully.",
        "result": result
    }

@app.get("/user_by_email/{email}/{org}")
def get_user_by_email(email: str, org: str):
    """
    Endpoint to retrieve a user by their email for the organization.

    Parameters:
        email (str): The email of the user.
        org (str): The organization of the user.

    Returns:
        dict: The user object if found, otherwise an error message.
    """
    logger.info(f"Retrieving user with email: {email} for organization: {org}")
    user = return_user_by_email(email, org)
    if user:
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": "protected",
            "email": user.email,
            "org": user.org
        }
    else:
        logger.warning(f"No user found with email: {email} for organization: {org}")
