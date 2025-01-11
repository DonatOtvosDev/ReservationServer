from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

import database.modells.calendar_modells as models

def get_day_by_id(db:Session, day_id:int) -> models.Day:
    """
    This function returns the day with the id given from the database under db session
    """
    return db.query(models.Day).filter(models.Day.id == day_id).first()

def get_day_by_date(db:Session, date:date) -> models.Day:
    """
    This function returns the day with the date given from the database under db session
    """
    return db.query(models.Day).filter(models.Day.date == date).first()

def update_day_workingday_id(db:Session, day_id:int, working_day:bool) -> None:
    """
    This function updatest the working_day property of thad iy with the id to the wroking_day specified from the database under db session
    """
    db.query(models.Day).filter(models.Day.id == day_id).update({"working_day":working_day}, synchronize_session=False)
    db.commit()
    
def get_working_days(db:Session, skip:int, limit:int) -> list[models.Day]:
    """
    This function returns all tha days that have not passed and have the working day property true in the database under db session
    """
    return db.query(models.Day).filter(models.Day.date >= datetime.now() - timedelta(hours=24)).filter(models.Day.working_day == True).offset(offset=skip).limit(limit=limit).all()

def create_day(db:Session, day:dict) -> models.Day:
    """
    This function creates a day object in the database under db session
        day: its a dictionary containing all the information needed [date, day_name, month_id]
    """
    db_day = models.Day(
        date = day["date"],
        day_name = day["day_name"],
        month_id = day["month_id"]
    )
    db.add(db_day)
    db.commit()
    db.refresh(db_day)

    return db_day