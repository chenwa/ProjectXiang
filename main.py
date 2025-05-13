from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.openapi.utils import get_openapi
import logging
from utils.logger import setup_logging
from dtos.user_dto import UserDTO
from dtos.address_dto import AddressDTO
from manage_user import (
    add_user,
    add_user_address,
    authenticate_user_password,
    get_user_by_id,
    delete_user_by_email,
    search_users_by_name,
    update_user_name_by_email,
    return_user_by_email,
    get_user_id_by_email
)
import pandas as pd

setup_logging()
logger = logging.getLogger('my_module')

# Secret key for session management
SECRET = "123"
manager = LoginManager(SECRET, token_url="/login")

@manager.user_loader()
def load_user(email: str):
    """
    Load user from the database using their email.

    Parameters:
        email (str): The email of the user.

    Returns:
        dict or None: The user object if found, otherwise None.
    """
    logger.info(f"Attempting to load user with email: {email}")

    user = return_user_by_email(email)
    if user:
        logger.info(f"User found: {user.email}")
        return user.email
    logger.warning(f"No user found")
    return None

app = FastAPI()

@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint to authenticate a user and return a session token.

    Parameters:
        email (str): The email of the user.
        password (str): The plaintext password of the user.

    Returns:
        dict: A session token if authentication is successful.
    """
    email = data.username
    password = data.password

    logger.info(f"Validating user: {email}")
    if not authenticate_user_password(email, password):
        raise InvalidCredentialsException

    # Create the token with the user's email as the subject
    access_token = manager.create_access_token(data={"sub": email})
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

@app.post("/users_create/")
def create_user(user: UserDTO, address: AddressDTO):
    """
    Endpoint to create a new user and their address.

    Parameters:
        user (UserDTO): The user model containing user details.
        address (AddressDTO): The address DTO containing address details.

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
    logger.info(f"Adding address for user ID: {address.user_id}")

    # Ensure the authenticated user matches the user_id in the address
    user_id = get_user_id_by_email(user)
    if user_id != address.user_id:
        return {"error": "You are not authorized to add an address for this user."}

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

@app.get("/user_by_email/{email}")
def get_user_by_email_endpoint(email: str):
    """
    Endpoint to retrieve a user by their email.

    Parameters:
        email (str): The email of the user.

    Returns:
        dict: The user object if found, otherwise an error message.
    """
    logger.info(f"Retrieving user with email: {email}")
    user = return_user_by_email(email)
    if user:
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password": "protected",
            "email": user.email
        }
    else:
        logger.warning(f"No user found with email: {email}")

@app.post("/bulk_upload_users/")
def bulk_upload_users(file: UploadFile = File(...)):
    """
    Endpoint to bulk upload users from a CSV file.

    Parameters:
        file (UploadFile): The uploaded CSV file containing user data.

    Returns:
        dict: A summary of the bulk upload process.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file.file)

        # Validate required columns
        required_columns = ["first_name", "last_name", "email", "password"]
        if not all(column in df.columns for column in required_columns):
            raise HTTPException(status_code=400, detail=f"CSV file must contain the following columns: {', '.join(required_columns)}")

        # Iterate through the rows and create users
        created_users = []
        failed_users = []
        for _, row in df.iterrows():
            try:
                # Create a UserDTO object
                user_dto = UserDTO(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    password=row["password"]
                )

                # Create a dummy address for the user
                address_dto = AddressDTO(
                    user_id=1,
                    street="123 Default St",
                    city="Default City",
                    state="Default State",
                    zip_code="00000",
                    country="Default Country"
                )

                # Add the user to the database
                new_user = add_user(user_dto, address_dto)
                if new_user:
                    created_users.append(row["email"])
                else:
                    failed_users.append(row["email"])
            except Exception as e:
                logger.error(f"Failed to create user {row['email']}: {e}")
                failed_users.append(row["email"])

        return {
            "message": "Bulk upload completed.",
            "created_users": created_users,
            "failed_users": failed_users
        }

    except Exception as e:
        logger.error(f"Error processing bulk upload: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")
