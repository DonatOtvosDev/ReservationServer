from datetime import datetime
from sqlalchemy.orm import Session

import database.modells.appointment_modells as models

def get_reservation_by_id(db:Session, reservation_id:int) -> models.Reservation:
    """
    This function retruns the reservation with the sepcified id from the database under db session
    """
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def get_reservations_userid(db:Session, user_id:int) -> list[models.Reservation]:
    """
    This function retruns the reservations with the given user id from the database under db session
    """
    return db.query(models.Reservation).filter(models.Reservation.user_id == user_id).order_by(models.Reservation.submitted).all()

def delete_reservation(db:Session, reservation_id:int) -> None:
    """
    This function deletes the reservation sepcifided id from the database under db session
    """
    db.query(models.Reservation).filter(models.Reservation.id == reservation_id).delete()

def delete_userinfo(db:Session, user_id:int) -> None:
    """
    This function deletes all the reservation connected to the specified user id from the database under db session
    """
    db.query(models.Reservation).filter(models.Reservation.user_id == user_id).delete()
    db.commit()

def add_reservation(db:Session, appointent_id:int, reservation_data:dict, user_id:int) -> models.Reservation:
    """
    This function creates a reservation under the appointemnt specified with the user id and reservation data provided in the database under db session
    """
    db_reservation = models.Reservation(
        user_id = user_id,
        reservation_data = reservation_data,
        appointment_id = appointent_id,
        submitted = datetime.utcnow()
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation
