from sqlalchemy.orm import Session
from datetime import datetime

import database.modells.calendar_modells as models

def get_months(db:Session, limit:int, offset:int, year:int):
    """
    This function returns and filters if porvided, the months at the offset with the given limit form the database under db session
    """
    if year == None:
        return db.query(models.Month).filter(models.Month.to_date > datetime.now()).order_by(models.Month.key).offset(offset).limit(limit).all()

    return db.query(models.Month).filter(models.Month.year == year).order_by(models.Month.key).limit(limit=limit).all()

def get_month_by_id(db:Session, month_id:int) -> models.Month:
    """
    This function retruns the month with the sepcified id from the database under db session
    """
    return db.query(models.Month).filter(models.Month.id == month_id).first()

def get_month_by_key(db:Session, month_key:int) -> models.Month:
    """
    This function retruns the month with the sepcified key from the database under db session
    """
    return db.query(models.Month).filter(models.Month.key == month_key).first()

def create_month(db:Session, month:dict) -> models.Month:
    """
    This function creates a month object in the the database under db session
        month: A dinctionary containing the needed information [key, month_number, year, month_name, from_date, to_date]
    """
    db_month = models.Month(
        key= month["key"],
        month_number = month["month_number"],
        year = month["year"],
        month_name = month["month_name"],
        from_date = month["from_date"],
        to_date = month["to_date"]
        )
    db.add(db_month)
    db.commit()
    db.refresh(db_month)
    
    return db_month