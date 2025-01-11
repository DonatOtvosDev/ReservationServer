from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from reps.database_reps.database_services import get_db

import database.schemas.AuthSchemas as AuthSchemas
import database.schemas.AppointmentSchemas as AppointmentSchemas

import reps.standad_reps.appointmentReps as appointmentReps


router = APIRouter()

@router.get("/appointment/{id}", response_model=AppointmentSchemas.Appointment ,tags=["Appointemnt"], status_code=200)
async def get_appointment(id:int, db:Session=Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return appointmentReps.get_appointment(access_token=token, appointment_id=id, db_session=db)

@router.post("/appointment/create", response_model=AppointmentSchemas.BaseAppointment, tags=["Appointemnt"], status_code=201)
async def add_apointment(token:AuthSchemas.Token, appointment:AppointmentSchemas.AddAppointment, db:Session = Depends(get_db)):
    return appointmentReps.add_appointment(token=token, appointment=appointment, db_session=db)

@router.delete("/appointment/delete", tags=["Appointemnt"], status_code=202)
async def delete_appointment(token:AuthSchemas.Token, appointment:AppointmentSchemas.DeleteAppointment, db:Session=Depends(get_db)):
    return appointmentReps.delete_appointment(token=token, appointment_id=appointment.appointment_id, db_session=db)
