from sqlalchemy.orm import Session
from fastapi import HTTPException 
from database.schemas.AppointmentSchemas import AddAppointment, Appointment
from database.schemas.ServiceSchemas import Service
from datetime import datetime

from database.schemas.AuthSchemas import Token
from reps.standad_reps.userReps import verify_user

import reps.database_reps.db_day as db_day
import reps.database_reps.db_appointment as db_appointment
import reps.database_reps.db_reservation as db_reservation

def get_appointment(access_token:str, appointment_id:int, db_session:Session) -> Appointment:
    """
    This function retuns the appointment at the given id and raises error if not
        Requires: 
            access_token: JWTToken generated at login
            appointment_id: The id of the appointment
            db_session: A database session that provides access to the database
    """
    user = verify_user(db_session=db_session, access_token=access_token, return_user=True)

    db_item =  db_appointment.get_appointent_by_id(db=db_session, appointment_id=appointment_id)
    if db_item == None:
        raise HTTPException(status_code=404,detail="Appointent not found with this id" )
    #Checking if the appointment is in the database

    response = {
        "id": db_item.id,
        "starts": db_item.starts,
        "ends": db_item.ends,
        "status": db_item.status,
        "day_id": db_item.day_id,
        "reservations": []
    }
    #Generating the response based on the 
    
    if db_item.status == "free":
        return response
    #Sending response if the appointment is free

    elif user.id == db_item.reservation[0].user_id or user.access_level == "admin":
        response["reservations"] = [db_item.reservation[0].__dict__]
        response["reservations"][0]["reservation_data"] = Service.parse_obj(db_item.reservation[0].reservation_data)
        return response
    #Adding the reservation data if the person has access
    
    else:
        return response
    #Responding if no access to the reservation data

def add_appointment(token:Token, appointment : AddAppointment, db_session:Session) -> Appointment:
    """
    The function validates the appointment data provided and adds an apointment to the database 
        Requires: 
            access_token: JWTToken generated at login (ADMIN)
            appointment: Appointment data based on the AddApointment schema,
            db_session: A database session that provides access to the database
        The day with the given id has to be available and the time period has to be free
    """
    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)

    day = db_day.get_day_by_id(db=db_session, day_id=appointment.day_id)
    if day == None:
        raise HTTPException(status_code=404, detail="Day with this id is not found")
    if day.date < datetime.now().date():
        raise HTTPException(status_code=406, detail="You cannot add appointment to day that is already passed")
    if appointment.starts.date() != day.date or appointment.ends.date() != day.date:
        raise HTTPException(status_code=406, detail="The date of the appointment is not the same with the day it is booked for")
    #Checking if the day is available for booking and the information about the date provided is correct

    if appointment.starts > appointment.ends:
        raise HTTPException(status_code=406, detail="The starting time is after the ending")
    #Checking if the appointemnt times are valid it does not starts before it ends

    for apoint in day.appointments:
        if apoint.starts.replace(tzinfo=None) < appointment.starts.replace(tzinfo=None) and apoint.ends.replace(tzinfo=None) > appointment.starts.replace(tzinfo=None):
            raise HTTPException(status_code=406, detail="There is an appointment at this time")
        if apoint.starts.replace(tzinfo=None) > appointment.starts.replace(tzinfo=None) and apoint.starts.replace(tzinfo=None) < appointment.ends.replace(tzinfo=None):
            raise HTTPException(status_code=406, detail="There is an appointment at this time")
    #Checking if the time period is free or not, timezone is set to zero because it cannot be compared if it is not the same, both shoud be utc by default when inputed

    db_day.update_day_workingday_id(db=db_session, day_id=appointment.day_id, working_day=True)
    #Setting the day to a working day

    db_item = db_appointment.create_appointment(
        starts=appointment.starts,
        ends=appointment.ends,
        day_id=appointment.day_id,
        db=db_session
    )
    
    response = {
        "id": db_item.id,
        "starts" : db_item.starts,
        "ends" : db_item.ends,
        "status" : db_item.status,  
        "day_id" : db_item.day_id,
    }
    #Responding based on the new item created in the database    
    return response


def delete_appointment(token:Token, appointment_id:int, db_session:Session):
    """
    This function deletes the appointment at the given id
        Requires: 
            access_token: JWTToken generated at login (ADMIN)
            appointment_id: The id of the appointment
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)

    db_item = db_appointment.get_appointent_by_id(db=db_session, appointment_id= appointment_id)
    if db_item == None:    
        raise HTTPException(status_code=404, detail="Appointntment with this id is not found")
    #Checking if the appointent exist
    if db_item.status == "reserved":
        db_reservation.delete_reservation(db=db_session, reservation_id=db_item.reservation[0].id)
    #Deleting reservation if it exist

    day = db_day.get_day_by_id(db=db_session, day_id=db_item.day_id)

    db_appointment.delete_appointment(db=db_session, appointment_id=appointment_id)

    if day.appointments == []:
        db_day.update_day_workingday_id(db=db_session, day_id=day.id, working_day=False)
    #Changing day status if no appointemnt after deletition
