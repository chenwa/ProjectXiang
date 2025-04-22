import logging
from utils.logger import setup_logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from db_session import Session, User

setup_logging()
logger = logging.getLogger('my_module')

def get_user_by_id(user_id: int):
    """
    Return a User instance by its id.
    
    Parameters:
        user_id (int): The ID of the user to retrieve.
    
    Returns:
        User: The User object if found, otherwise None.
    """
    # Create a new session
    session = Session()
    try:
        # Option 1: Using Session.get() (SQLAlchemy 2.0+)
        user = session.get(User, user_id)
        
        # Option 2: Alternatively, using filter_by:
        # user = session.query(User).filter_by(id=user_id).first()
        
        return user
    finally:
        # Always close the session to free resources.
        session.close()

def add_user(name: str, email: str):
    """
    Creates a new user in the database.
    
    Parameters:
        name (str): The name of the user.
        email (str): The email of the user.
    
    Returns:
        User: The newly created User object.
    """
    session = Session()
    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        session.commit()
        logger.info(f"User created with ID {new_user.id}")
        return new_user
    except Exception as e:
        session.rollback()  # Rollback any changes if error occurs.
        logger.error("Error creating user:", e)
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
        session.rollback()  # Rollback if an error occurs.
        logger.error("Error deleting user:", e)
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
            user.name = new_name  # Update the name
            session.commit()
            logger.info(f"User with email {email} has been updated to name {new_name}.")
            return True
        else:
            logger.info(f"No user found with email {email}.")
            return False
    except Exception as e:
        session.rollback()  # Rollback if an error occurs
        logger.error("Error updating user:", e)
        return False
    finally:
        session.close()

# Function to Search Users by Name
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
        # Use the `ilike` operator for a case-insensitive search
        matching_users = session.query(User).filter(User.name.ilike(f"%{query}%")).all()
        
        # Logging or debugging output
        if matching_users:
            logger.info(f"Found {len(matching_users)} users matching '{query}':")
            for user in matching_users:
                logger.info(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
        else:
            logger.info(f"No users found matching '{query}'.")
            
        return matching_users
    except Exception as e:
        logger.error("Error during search:", e)
        return []
    finally:
        session.close()

