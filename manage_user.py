import logging
import bcrypt
from utils.limiter import rate_limiter
from utils.logger import setup_logging
from db.session_objects import Session, User, Address
from dtos.address_dto import AddressModel
from dtos.user_dto import UserModel

setup_logging()
logger = logging.getLogger('my_module')


@rate_limiter(max_requests=1, time_window=60)
def get_user_by_id(user_id: int):
    """
    Return a User instance by its id.

    Parameters:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The User object if found, otherwise None.
    """
    session = Session()
    try:
        user = session.get(User, user_id)
        return user
    finally:
        session.close()


def add_user(user: UserModel, address: AddressModel):
    """
    Creates a new user in the database with an encrypted password.
    Then adds address to the newly created user.

    Parameters:
        user (UserModel): A model containing first_name, last_name, email,
                          and password.
        address (AddressModel): A model containing street, city, state,
                                zip_code, and country.

    Returns:
        User: The newly created User object.
    """
    session = Session()
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            encrypted_password=hashed_password.decode('utf-8')
        )

        session.add(new_user)
        session.commit()
        logger.info(f"User created with ID {new_user.id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {e}")
        return None
    finally:
        session.close()

    new_user_id = find_user_id_by_email(user.email)
    if new_user_id:
        address_result = add_user_address(
            new_user_id,
            address.street,
            address.city,
            address.state,
            address.zip_code,
            address.country
        )
        logger.info(f"Address add result: {address_result}")
    else:
        logger.error("Failed to locate new user to add address.")

    return new_user


def add_user_address(user_id: int, street: str, city: str, state: str, zip_code: str, country: str):
    """
    Adds a new address for a specified user.

    Parameters:
        user_id (int): The ID of the user to associate with the address.
        street (str): The street address.
        city (str): The city name.
        state (str): The state/province name.
        zip_code (str): The postal/zip code.
        country (str): The country name.

    Returns:
        dict: A message indicating success or failure.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            logger.info(f"No user found with ID {user_id}.")
            return {"error": "User not found"}

        new_address = Address(
            user_id=user_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country
        )

        session.add(new_address)
        session.commit()
        logger.info(f"Address added for user ID {user_id}.")
        return {"message": "Address added successfully", "address_id": new_address.id}
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding address for user ID {user_id}: {e}")
        return {"error": "Failed to add address"}
    finally:
        session.close()


def authenticate_user_password(email: str, password: str):
    """
    Authenticates a user by checking if the provided password matches
    the stored hashed password for the given email.

    Parameters:
        email (str): The email of the user.
        password (str): The plaintext password provided by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            logger.info(f"No user found with email {email}.")
            return False

        stored_hashed_password = user.encrypted_password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            logger.info("Authentication successful!")
            return True
        else:
            logger.info("Authentication failed: Incorrect password.")
            return False
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        return False
    finally:
        session.close()


def delete_user_by_email(email: str):
    """
    Deletes a user from the database based on their email.

    Parameters:
        email (str): The email of the user to delete.

    Returns:
        bool: True if the user was deleted, False if no user was found.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            session.delete(user)
            session.commit()
            logger.info(f"User with email {email} has been deleted.")
            return True
        else:
            logger.info(f"No user found with email {email}.")
            return False
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting user: {e}")
        return False
    finally:
        session.close()


def update_user_name_by_email(email: str, new_name: str):
    """
    Updates a user's name in the database based on their email.

    Parameters:
        email (str): The email of the user to update.
        new_name (str): The new name to assign.

    Returns:
        bool: True if the update was successful, False if no user was found.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            user.first_name = new_name
            session.commit()
            logger.info(f"User with email {email} has been updated to name {new_name}.")
            return True
        else:
            logger.info(f"No user found with email {email}.")
            return False
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating user: {e}")
        return False
    finally:
        session.close()


def search_users_by_name(query: str):
    """
    Searches for users whose names include the given query (case-insensitive).

    Parameters:
        query (str): The substring to search for in the user's name.

    Returns:
        list[User]: A list of matching User objects.
    """
    session = Session()
    try:
        matching_users = session.query(User).filter(User.first_name.ilike(f"%{query}%")).all()

        if matching_users:
            logger.info(f"Found {len(matching_users)} users matching '{query}':")
            for user in matching_users:
                logger.info(f"ID: {user.id}, Name: {user.first_name}, Email: {user.email}")
        else:
            logger.info(f"No users found matching '{query}'.")

        return matching_users
    except Exception as e:
        logger.error(f"Error during search: {e}")
        return []
    finally:
        session.close()


def find_user_id_by_email(email: str):
    """
    Finds and returns the ID of the user with the given email.

    Parameters:
        email (str): The email address of the user.

    Returns:
        int or None: The user's ID if found, otherwise None.
    """
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if user:
            logger.info(f"User found with email {email}: ID {user.id}")
            return user.id
        else:
            logger.info(f"No user found with email {email}.")
            return None
    except Exception as e:
        logger.error(f"Error finding user by email: {e}")
        return None
    finally:
        session.close()



