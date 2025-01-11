from sqlalchemy.orm import Session

import database.modells.service_modells as models
from database.schemas.ServiceSchemas import ServiceCreate

def get_services(db:Session) -> list[models.Service]:
    """
    This function retruns all the services from the database under db session
    """
    return db.query(models.Service).all()

def get_service_by_id(db:Session, service_id:int) -> models.Service:
    """
    This function returns the service with the id from the database under db session
    """
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def update_service(db:Session, service_id:int, to_update :dict):
    """
    This function updates the service with the id with the provided attributes from the database under db session
    """
    db.query(models.Service).filter(models.Service.id == service_id).update(to_update, synchronize_session=False)
    db.commit()

def delete_service(db:Session, service_id:int)->None:
    """
    This function deletes the service with the id from the database under db session
    """
    db.query(models.Service).filter(models.Service.id == service_id).delete()
    db.commit()

def create_service(db:Session, service : ServiceCreate) -> models.Service:
    """
    This function creates a service based on the service provided with the schema ServiceCreate in the database under db session
    """
    db_service = models.Service(
        name = service.name,
        service_type = service.service_type,
        description = service.description,
        comment = service.comment,
        price = service.price,
        lenght = service.lenght
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service