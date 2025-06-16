from dotenv import load_dotenv
load_dotenv()
import os
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import (
        create_engine,
        Column,
        Integer,
        String,
        DateTime,
        func,
        ForeignKey
        )

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. Please define it in your .env file.")
engine = create_engine(DATABASE_URL)
# Base class for ORM models
Base = declarative_base()

# Define your ORM model corresponding to the "users" table.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    encrypted_password = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)  
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Establish bidirectional relationship with Address
    addresses = relationship("Address", back_populates="user",
                             cascade="all, delete-orphan", lazy="joined")

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)  # Primary key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=False)

    # Establish bidirectional relationship with User
    user = relationship("User", back_populates="addresses")

# Create a session factory
Session = sessionmaker(bind=engine)


