from fastapi import HTTPException
from sqlalchemy.orm import Session
import re

from database.schemas.AuthSchemas import Token
from database.schemas.ServiceSchemas import Service
from reps.standad_reps.userReps import verify_user

import database.schemas.ServiceSchemas as Schemas
import reps.database_reps.db_services as db_services

def get_services(db_session : Session) -> dict[str : list[Service]]:
    """
    This function returns all the services stored in the database
        Requires:
            db_session: A database session that provides access to the database
        It returns a dictionary with the types of services being the key refering to a list of services included under that type
        {str (type of service) : list[Service]}
    """
    services = db_services.get_services(db=db_session)
    response = {}

    for service in services:
        if not (service.service_type in response.keys()):
            response[service.service_type] = []
        response[service.service_type].append({"id":service.id,
        "name":service.name,
        "service_type":service.service_type,
        "description":service.description,
        "price":service.price,
        "comment":service.comment,
        "lenght":service.lenght})
    #using the different service types it groups the services

    return response

def update_service(token:Token, service:Schemas.ServiceUpdate, db_session:Session):
    """
    This function updates the infromation that is different in the database for the the service provided
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            service: Data provided for updatimng based on the SercviceUpdate Schema
            db_session: A database session that provides access to the database
    """

    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)

    service_db = db_services.get_service_by_id(db=db_session, service_id=service.id)
    if service_db == None:
        raise HTTPException(status_code=404, detail="Service with this id is not found")
    #Checking if service with the id exist

    updated_service = {}
    something_to_update = False
    #Defining the paramaters that helps validateing and updating later

    if service.name != None and service_db.name != service.name:
        if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ ]", string=service.name)):
            raise HTTPException(status_code=406, detail="Invalid service name")
        updated_service["name"] = service.name
        something_to_update = True
        
    if service.service_type != None and service_db.service_type != service.service_type:
        if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=service.service_type)):
            raise HTTPException(status_code=406, detail="Invalid service type")
        updated_service["service_type"] = service.service_type
        something_to_update = True

    if service.description != None and service_db.description != service.description:
        if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\.\?\-\+\:\'\!\%\n\,\" ]", string=service.description)):
            raise HTTPException(status_code=406, detail="Invalid service description")
        updated_service["description"] = service.description
        something_to_update = True
     
    if service.comment != None and service_db.comment != service.comment:
        if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\+\/\- ]", string=service.comment)):
            raise HTTPException(status_code=406, detail="Invalid comment")
        updated_service["comment"] = service.comment
        something_to_update = True

    if service.price != None and service_db.price != service.price:
        updated_service["price"] = service.price
        something_to_update = True

    if service.lenght != None and service_db.lenght != service.lenght:
        updated_service["lenght"] = service.lenght
        something_to_update = True

    #Cheking if the parameter is changed in the data provided or exist and adds it to the parameters update
    #something_to_update is set to true if there is any new parameter
    
    if something_to_update == False:
        raise HTTPException(status_code=406, detail="Parameters provided are not enough to update the service")
    #Cheking if the parameters provided at least contains one new element or raises error

    db_services.update_service(db=db_session, service_id=service.id, to_update=updated_service)


def create_service(token:Token, service:Schemas.ServiceCreate, db_session:Session) -> Schemas.Service:
    """
    This function validates the input provided and adds a service based on that data if it is valid
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            service: The service data for adding to the database based on the ServiceCreate schema
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)

    if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ ]", string=service.name)):
        raise HTTPException(status_code=406, detail="Invalid service name")

    if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=service.service_type)):
        raise HTTPException(status_code=406, detail="Invalid service type")

    if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\.\?\-\+\:\'\!\%\n\,\" ]", string=service.description)):
        raise HTTPException(status_code=406, detail="Invalid service description")
    
    if service.comment != None:
        if len(re.findall(pattern="[^a-zA-záéíóöőúüűÁÉÍÓÖŐÚÜŰ\+\/\- ]", string=service.comment)):
            raise HTTPException(status_code=406, detail="Invalid service comment")
    #Validating the strings with regex

    db_item = db_services.create_service(db=db_session, service=service)

    response = {
        "id":db_item.id,
        "name":db_item.name,
        "service_type":db_item.service_type,
        "description":db_item.description,
        "price":db_item.price,
        "comment":db_item.comment,
        "lenght":db_item.lenght
    }

    return response

def delete_service(token:Token, service_id:int, db_session:Session):
    """
    The function used to delete a service at the given id
     Requires:
            access_token: JWTToken generated at login (ADMIN)
            service_id: The id of the service that will be deleted
            db_session: A database session that provides access to the database
    """

    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)

    if db_services.get_service_by_id(db=db_session, service_id=service_id) == None:
        raise HTTPException(status_code=404, detail="Service with this id is not found")
    #Checking if the service exist

    db_services.delete_service(db=db_session, service_id=service_id)
