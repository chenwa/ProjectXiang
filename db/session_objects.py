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

def get_database_url():
    # 1. Use DATABASE_URL if set (Docker Compose, AWS ECS, or manual override)
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    # 2. Detect AWS ECS/Fargate (set your own env var in task definition if needed)
    if os.getenv("AWS_EXECUTION_ENV") or os.getenv("RDS_HOST"):
        # Use RDS connection string from environment variables
        user = os.getenv("RDS_USERNAME", "admin")
        password = os.getenv("RDS_PASSWORD", "projectxiang")
        host = os.getenv("RDS_HOST", "localhost")
        db = os.getenv("RDS_DB_NAME", "project_xiang")
        return f"mysql+pymysql://{user}:{password}@{host}/{db}"

    # 3. Default to local development
    return "mysql+pymysql://root:warren1928@localhost/project_xiang"

# Configure your connection settings
DATABASE_URL = get_database_url()

# Create an engine
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


