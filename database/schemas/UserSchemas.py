from pydantic import BaseModel


class UserBase(BaseModel):
    """The base of the other user schemas"""
    username : str
    email : str
    phone_number : str
    first_name : str
    sir_name : str

class ChangeUserInfo(BaseModel):
    """The information to update a service in the database"""
    password : str
    email : str = None
    phone_number : str = None
    first_name : str = None
    sir_name : str = None
class CreateUser(UserBase):
    """The user information with the password of the user"""
    password : str

class User(UserBase):
    """The user modell without the password"""
    id : int

class UserItem(User):
    """User with access level based on user schema"""
    access_level : str
class UserAdd(BaseModel):
    """The infromation needed to add access to a user"""
    id:int
class LoginUser(BaseModel):
    """The information needed to log in a user"""
    username : str
    password : str

class ChangePassword(BaseModel):
    """The infromation needed to change the password of a user"""
    old_password : str
    new_password : str 
