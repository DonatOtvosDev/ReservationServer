from pydantic import BaseModel

class Token(BaseModel):
    """The token schema containing the information for authentication after login"""
    access_token : str
    token_type : str

class TokenWithAccesLevel(Token):
    """The token schema containing the infromations for authentication and the duration before expiary furthermore the access level of the user"""
    access_level : str
    expiary_min : int