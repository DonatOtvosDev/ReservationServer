from pydantic import BaseModel

class DataToUpdate(BaseModel):
    """The structure of the data provided to change the data on the screen infos"""
    key : str
    content : str


class HomeScreenData(BaseModel):
    """This is the structure of the home screen data"""
    title : str
    subtitle : str
    slogan : str
    intro : str
    news : str
    description : str
    country : str
    county : str
    city : str
    postcode : str
    street : str
    housenum : str
    advertisement : str
    phone_number : str 
    email_adress : str

class AboutMeScreenData(BaseModel):
    """This is the structure of the aboutme screen data"""
    name : str
    brief_description : str
    longer_description : str
    educations : str
    my_vision : str