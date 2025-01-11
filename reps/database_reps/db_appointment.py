from datetime import datetime
from sqlalchemy.orm import Session

import database.modells.appointment_modells as models

def get_appointent_by_id(db:Session, appointment_id:int) -> models.Appointment:
    """
    This function returns the appointment with the given id from the database under db session
    """
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def update_appointent_status(db:Session, appointment_id:int, status:str) -> None:
    """
    This function updates the status of the appointment under the given id in the database under db session
    """
    db.query(models.Appointment).filter(models.Appointment.id == appointment_id).update({"status" : status}, synchronize_session=False)
    db.commit()

def create_appointment(db:Session, starts:datetime, ends:datetime, day_id:int) -> models.Appointment:
    """
    This function creates an appointment in the database under db session
        starts: The time the appointent starts
        ends: The time the appointent ends
        day_id: The id of the day which the appointent is on
    """
    db_appointment = models.Appointment(
        starts = starts,
        ends = ends,
        day_id = day_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment 

def delete_appointment(db:Session, appointment_id:int):
    """
    This function deletes an appointment that is at the given id in the database under db session
    """
    db.query(models.Appointment).filter(models.Appointment.id == appointment_id).delete(synchronize_session=False)
    db.commit()