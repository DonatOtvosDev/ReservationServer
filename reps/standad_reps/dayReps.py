from fastapi import HTTPException
from sqlalchemy.orm import Session

from datetime import date

import reps.database_reps.db_day as db_day
from database.modells.calendar_modells import Day
from database.schemas.DaySchemas import Day as daySchema
from reps.standad_reps.userReps import verify_user

def create_response(db_item:Day) -> dict:
    """This function creates a dictionary that can be returned as response based on the Day passed to it"""
    response = {
        "id" : db_item.id,
        "date" : db_item.date,
        "working_day" : db_item.working_day,
        "day_name" : db_item.day_name,
        "month_id" : db_item.month_id,
        "appointments" : [{ "id": appoint.id,
        "starts": appoint.starts,
        "ends": appoint.ends,
        "status": appoint.status,
        "day_id": appoint.day_id} for appoint in db_item.appointments]
    }
    return response


def get_day_id(access_token:str, day_id:int, db_session:Session) -> daySchema:
    """
    This function returns a day at a given id and raises error if not available
        Requires:
            access_token: JWTToken generated at login
            day_id: The id of the day requested
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=access_token)

    db_item = db_day.get_day_by_id(db=db_session, day_id=day_id)
    if db_item == None:
        raise HTTPException(status_code=404, detail="Day not found with this id")

    return create_response(db_item=db_item)

def get_day_date(access_token:str, date:date, db_session:Session) -> daySchema:
    """
    This function returns a day by date and raises error if not available
        Requires:
            access_token: JWTToken generated at login
            date: The date of the day requested
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=access_token)

    db_item = db_day.get_day_by_date(db=db_session, date=date)
    if db_item == None:
        raise HTTPException(status_code=404, detail="Day is not inatialized")

    return create_response(db_item=db_item)

def get_working_days(access_token:str, limit:int, skip:int, db_session:Session) -> list[Day]:
    """
    This function returns the working days those has at least one appointment
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            limit: The max lengt of the list returned
            skip: The appintents skipped before selecting the list returned
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=access_token, auth_admin=True)
    working_days = db_day.get_working_days(db=db_session, skip=skip, limit=limit)
    
    response = [{
        "id" : db_item.id,
        "date" : db_item.date,
        "working_day" : db_item.working_day,
        "day_name" : db_item.day_name,
        "month_id" : db_item.month_id} for db_item in working_days]
    
    return response