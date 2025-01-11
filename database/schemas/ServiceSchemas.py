from pydantic import BaseModel

class ServiceCreate(BaseModel):
    """The infromation needed to create a service"""
    name : str
    service_type : str
    description : str
    comment : str = None
    price : int
    lenght : int

class Service(ServiceCreate):
    """The modell of a service"""
    id : int

class DeleteService(BaseModel):
    """The information needed to delete a service"""
    id : int

class ServiceUpdate(BaseModel):
    """The monell of a data with optionakl fields for updating an already existing service"""
    id : int
    name : str = None
    service_type : str = None
    description : str = None
    comment : str = None
    price : int = None
    lenght : int = None