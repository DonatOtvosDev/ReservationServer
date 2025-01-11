from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The path to the database
SQLALCHEMY_DATABASE_URL = "sqlite:///database/database.db"

# Create an engine with check_same_thread set to False
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base for the database models
Base = declarative_base()