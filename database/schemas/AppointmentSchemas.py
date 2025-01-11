from pydantic import BaseModel
from datetime import datetime
from database.schemas.ReservationSchemas import Reservation

class AddAppointment(BaseModel):
    """The schema needed when the appointment needs to be added"""
    starts : datetime
    ends : datetime
    day_id : int

class DeleteAppointment(BaseModel):
    """The information needed when the the sender wants to delete an appointment"""
    appointment_id : int

class GetAppointment(BaseModel):
    """The information needed when the the sender wants to access an appointment"""
    appointment_id : int

class BaseAppointment(BaseModel):
    """The appointment modell without the reservations"""
    id : int
    starts : datetime
    ends : datetime
    status : str
    day_id : int

class Appointment(BaseAppointment):
    """The appointment modell with the reservations"""
    reservations : list[Reservation]

