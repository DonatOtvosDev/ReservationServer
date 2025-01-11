from datetime import datetime, timedelta
from jose import jwt, JWTError

from passlib.context import CryptContext

from database.schemas.AuthSchemas import Token, TokenWithAccesLevel

from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
#Creating the object used for hashing

def verify_password(planin_pasw : str, hashed_pasw : str) -> bool:
    """It checks if the two paswords are the same if hashed"""
    return password_ctx.verify(planin_pasw, hashed_pasw)


def hash_password(password : str):
    """The function hashes the password given"""
    return password_ctx.hash(password)


def create_access_token(user_name:str, user_id:int) -> dict:
    """
    This function is used to create an access token with the username and id included
        Returns a dictionary including:
            "access_token": it is the JWTToken
            "expiary_min": The expiary time of the token
            "token_type": The type of the token currently bearer
    """
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user":{"name":user_name,"id":user_id }, "expires": expire_time.isoformat()}
    #Setting the attributes of the token into variables

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token":token, "expiary_min":ACCESS_TOKEN_EXPIRE_MINUTES, "token_type":"bearer"}

def return_token_content(token:Token) -> dict | str:
    """This funtion returns the decoded content of the token or an error if the token is invalid"""
    try:
        content = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        content = "Error"
    return content