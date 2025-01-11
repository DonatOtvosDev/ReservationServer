from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from reps.database_reps.database import Base

class Appointment(Base):
    """
    This is the orm modell of the appointments
        id: The primary and unique identifier of an appointment
        starts: The starting time of the appointment
        ends: The ending time of the appointment
        status: The current status of the appointent [reserved, free, datadeleted]
        reservation: The reservation based on the reservation related to the appointment
    """
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    starts = Column(DateTime)
    ends = Column(DateTime)
    status = Column(String, default="free")
    day_id = Column(Integer, ForeignKey("days.id"))
    reservation = relationship("Reservation",back_populates="appointment")

    day = relationship("Day", back_populates="appointments")

class Reservation(Base):
    """
    This is the orm modell of the reservations 
        id: The primary and unique identifier of a reservation
        user_id: The id of the user submiting
        reservation_data: The service infromation stored in json format
        submitted: The time when the reservation was submitted
        appointment_id: The id of the appointment where the reservation was submitted
    """
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    reservation_data = Column(JSON)
    submitted = Column(DateTime)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    appointment = relationship("Appointment", back_populates="reservation")
    