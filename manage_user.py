from utils.logger import setup_logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from db_session import Session, User

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
        print(f"User created with ID {new_user.id}")
        return new_user
    except Exception as e:
        session.rollback()  # Rollback any changes if error occurs.
        print("Error creating user:", e)
    finally:
        session.close()

