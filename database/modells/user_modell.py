from sqlalchemy import Column, Integer, String

from reps.database_reps.database import Base

class User(Base):
    """
    This is the orm modell of the users
        id: The primary and unique identifier of an user
        password: The hased parssword
        email: The email adress of the user
        phone_number: The phone number of the user
        first_name: The first name of the user
        sir_name: The sir_name of the user
        access_level: The access level of hte user [admin, user, banneduser] this provides infromation for what they can they access in the database
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique= True)
    password = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String)
    first_name = Column(String)
    sir_name = Column(String)
    access_level = Column(String, default="none")
