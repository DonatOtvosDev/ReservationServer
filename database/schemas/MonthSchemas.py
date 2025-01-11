from datetime import date
from pydantic import BaseModel

from database.schemas.DaySchemas import DayBase

class getMonth(BaseModel):
    """The information schema to get and create a moth based on the month and year"""
    year: int
    month_number: int
    create_month: bool = False
    return_days: bool = False

class getMonthResponse(BaseModel):
    """The modell of months with the days"""
    id: int
    month_name: str
    from_date: date
    to_date: date
    days: list[DayBase]
    
class getMonthsItem(BaseModel):
    """The modell of months without the days"""
    id: int
    month_name: str
    from_date: date
    to_date: date

class deteleMonth(BaseModel):
    """The infromation needed to delete a month"""
    id:int


