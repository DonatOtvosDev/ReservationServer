from pydantic import BaseModel
from datetime import date
from database.schemas.AppointmentSchemas import BaseAppointment

class DayBase(BaseModel):
    """The day modell without the appointments"""
    id : int
    date : date
    working_day : bool
    day_name : str
    month_id : int
    

class Day(DayBase):
    """The day modell with the appointments"""
    appointments : list[BaseAppointment]