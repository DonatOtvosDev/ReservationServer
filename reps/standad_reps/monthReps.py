import calendar
import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database.modells.calendar_modells import Month
from database.schemas.MonthSchemas import getMonthsItem, getMonthResponse
from database.schemas.DaySchemas import Day

from database.schemas.AuthSchemas import Token
from reps.standad_reps.userReps import verify_user

import reps.database_reps.db_month as db_month
import reps.database_reps.db_day as db_day

def create_response(db_item:Month, return_days:bool) -> getMonthResponse | getMonthsItem:
    """
    This function creates a response based on the Month object provided
        Requires:
            db_item: The month object
            return_days: Decides if the days are returned form the month
            creating_month: This changes the status code of the response
    """
    response = {
            "id":db_item.id,
            "month_name":db_item.month_name,
            "from_date":db_item.from_date,
            "to_date":db_item.to_date,
            "days" : []
        }
    #Creating the basic response

    if return_days:
        response["days"] = [{
        "id" : dayobj.id,
        "date" : dayobj.date,
        "working_day" : dayobj.working_day,
        "day_name" : dayobj.day_name,
        "month_id" : dayobj.month_id,
    } for dayobj in db_item.days]
        
    #Adding days if required

    return response

def create_month_rep(token: Token, month_num: int, year: int, return_days: bool, db_session:Session) -> JSONResponse:
    """
    This function creates a month object in the database based on the year adn month number, 
    it validates the month before adds it to database
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            month_number: The number of the month in the year
            year: The year in form of integer
            return_days: This argument decised if days are returned with the month
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token, auth_admin=True)

    month_range = calendar.monthrange(year=year,month=month_num)
    #Getting the first and last day of the month

    date_from = datetime.date(year=year, month=month_num, day=1)
    date_to = datetime.date(year=year, month=month_num, day=month_range[1])
    #Getting the datetime of the first and last day of the month

    if date_to < datetime.datetime.date(datetime.datetime.now()):
        raise HTTPException(status_code=406, detail="Cannot create month that is already ended")
    #Checks if the month is already gone or can still be ceated

    if len(str(month_num)) < 2:
        key = int(str(year) + "0"+str(month_num))
    else :
        key = int(str(year) + str(month_num))
    #Creates a key that is the year and month number with two digit combined
    
    if db_month.get_month_by_key(db=db_session, month_key=key) != None:
        raise HTTPException(status_code=409, detail="Month already exist in the database")
    #Checks if the month is already in the database

    month_name = date_from.strftime("%B")

    db_item = db_month.create_month(db=db_session, month={
        "key":key,
        "month_number":month_num,
        "year":year,
        "month_name":month_name,
        "from_date":date_from,
        "to_date":date_to
    })
    #Creating the month object
    for day_num in range(1, date_to.day + 1):
        date = datetime.date(year=db_item.year, month=db_item.month_number, day=day_num)
        day_name = date.strftime("%A")
        month_id = db_item.id

        db_day.create_day(db=db_session, day={
            "date":date,
            "day_name":day_name,
            "month_id":month_id
        })
    #Creating all the days to the database

    return JSONResponse(status_code=201, content=create_response(db_item=db_item, return_days=return_days))
    #Returning Json response with correct status code

def get_month_by_key(token:Token, month_num:int, year:int, return_days:bool, db_session:Session) -> JSONResponse:
    """
    This function returns the month from tha database using the key created by the year and month number, 
    checks if exists and raises error if not
        Requires:
            access_token: JWTToken generated at login
            month_number: The number of the month in the year
            year: The year in form of integer
            return_days: This argument decised if days are returned with the month
            db_session: A database session that provides access to the database
    """

    verify_user(db_session=db_session, access_token=token)
    if len(str(month_num)) < 2:
        key = int(str(year) + "0"+str(month_num))
    else :
        key = int(str(year) + str(month_num))
    #Creates a key that is the year and month number with two digit combined

    db_item = db_month.get_month_by_key(month_key=key, db=db_session)

    if db_item == None:
        raise HTTPException(status_code=404, detail="Month with this year and month number did not found")
    #Checks if the month exists

    response = create_response(db_item=db_item, return_days=return_days)
    if not return_days :
        response["days"] = []
    #Adding the empty list to satisfy the response shema if there are no days returned

    return JSONResponse(status_code=200, content=response)


def get_month_by_id(token:Token, month_id:int, return_days:bool, db_session:Session):
    """
    This function returns the month with the given id if it exists and raises error if not
        Requires:
            access_token: JWTToken generated at login
            month_id: The Id of the month requested
            return_days: This argument decised if days are returned with the month
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token)
    db_item = db_month.get_month_by_id(db=db_session, month_id=month_id)

    if db_item == None:
        raise HTTPException(status_code=404, detail="Month with this id is not found")
    #Checking if day with this id is avaialable

    return create_response(db_item=db_item, return_days=return_days)

def get_months(token:Token, db_session:Session, year:int, limit:int, skip:int) -> list[getMonthsItem]:
    """
    This function returns the months available in the database
        Requires:
            access_token: JWTToken generated at login
            limit: The max lengt of the list returned
            skip: The appintents skipped before selecting the list returned
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token)
    months = db_month.get_months(db=db_session, year=year, limit=limit, offset=skip)

    response = []
    
    for month in  months:
        response.append(
            create_response(db_item=month, return_days=False)
        )
    #Adding the days to the response
    return response

   
 