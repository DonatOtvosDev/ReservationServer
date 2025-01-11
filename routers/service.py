from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database.schemas.AuthSchemas import Token
from reps.database_reps.database_services import get_db

import database.schemas.ServiceSchemas as ServiceSchemas
import reps.standad_reps.serviceReps as serviceReps

router = APIRouter()

@router.get("/services", response_model=dict[str , list[ServiceSchemas.Service]], tags=["Service"], status_code=202)
async def get_services(db:Session = Depends(get_db)):
    return serviceReps.get_services(db_session=db)

@router.post("/service/create", response_model=ServiceSchemas.Service, tags=["Service"], status_code=201)
async def create_service(token:Token, service:ServiceSchemas.ServiceCreate, db:Session=Depends(get_db)):
    return serviceReps.create_service(token=token, service=service, db_session=db)

@router.post("/service/update", tags=["Service"], status_code=202)
async def update_service(token:Token, service:ServiceSchemas.ServiceUpdate, db:Session=Depends(get_db)):
    return serviceReps.update_service(token=token, service=service, db_session=db)

@router.delete("/service/delete", tags=["Service"], status_code=202)
async def delete_service(token:Token, service:ServiceSchemas.DeleteService, db:Session=Depends(get_db)):
    return serviceReps.delete_service(token=token, service_id=service.id, db_session=db)