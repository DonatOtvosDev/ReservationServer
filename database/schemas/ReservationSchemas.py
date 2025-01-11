from datetime import datetime
from pydantic import BaseModel
from database.schemas.ServiceSchemas import Service


class AddReservation(BaseModel):
    """The information needed to create a reservation"""
    appointment_id : int
    reservation_data : Service
class DeleteReservation(BaseModel):
    """The information needed to delete a reservation"""
    reservation_id : int
class Reservation(BaseModel):
    """The modell of a reservation"""
    id : int
    user_id : int
    appointment_id : int
    submitted : datetime
    reservation_data : Service
