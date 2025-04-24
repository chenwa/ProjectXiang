from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure your connection settings
DATABASE_URL = "mysql+pymysql://root:warren1928@localhost/project_xiang"

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

# Define the declarative base
Base = declarative_base()

# Define your ORM model corresponding to the "users" table.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    encrypted_password = Column(String(255))

# Create a session factory
Session = sessionmaker(bind=engine)


