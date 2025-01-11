from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import database.schemas.ReservationSchemas as ReservationSchemas
from database.modells.appointment_modells import Reservation

from database.schemas.AuthSchemas import Token
from reps.standad_reps.userReps import verify_user

import reps.database_reps.db_appointment as db_appointment
import reps.database_reps.db_reservation as db_reservation
import reps.database_reps.db_services as db_service
import reps.database_reps.db_user as db_user

def create_response(db_item:Reservation) -> ReservationSchemas.Reservation:
    """
    This function creates a response based on the reservation schema
    """
    response = {
        "id":db_item.id,
        "user_id":db_item.user_id,
        "appointment_id":db_item.appointment_id,
        "submitted":db_item.submitted,
        "reservation_data": db_item.reservation_data
    }
    #Creating the response
    return response

def get_reservation_by_id(token:str, reservation_id:int, db_session:Session) -> ReservationSchemas.Reservation:
    """
    This function returns the reservation at the given id if not found raises an exeption.
    Only owner of the reservation or admin can access the reservation
        Required:
            access_token: JWTToken generated at login
            reservation_id: The id of the resevation
            db_session: A database session that provides access to the database
    """
    user = verify_user(db_session=db_appointment, access_token=token, return_user=True)

    reservation = db_reservation.get_reservation_by_id(db=db_session, reservation_id=reservation_id)

    if reservation == None:
        raise HTTPException(status_code=404, detail="Reservation with this id is not found")
    #Checking if the reservation is available
    if reservation.user_id != user.id and user.access_level != 'admin':
        raise HTTPException(status_code=401, detail="You are not allowed to view this reservation")
    #Checking for access

    return create_response(db_item=reservation)

def get_reservations_user(token:str, db_session:Session) -> list[ReservationSchemas.Reservation]:
    """
    This function returns the reservations of the owner of the token
        Requires:
            access_token: JWTToken generated at login
            db_session: A database session that provides access to the database
    """
    user = verify_user(db_session=db_session, access_token=token, return_user=True)

    reservations = db_reservation.get_reservations_userid(db=db_session, user_id=user.id)

    response = [create_response(reservation) for reservation in reservations]

    return response

def get_reservations_admin_by_user(token:str, user_id:int, db_session:Session) -> list[ReservationSchemas.Reservation]:
    """
    This fucntion returns the reservations connected to the user with the userid provided
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            user_id: The id of the user asked
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=token, auth_admin=True)

    user = db_user.get_user_by_id(db=db_session, user_id=user_id)

    if user == None:
        raise HTTPException(status_code=404, detail="User with this id is not found")
    #Checking if the user exist

    if user.access_level == "admin":
        raise HTTPException(status_code=406, detail="Admins dont have reservaitions")
    #Checking if the user is not an admin

    reservations = db_reservation.get_reservations_userid(db=db_session, user_id=user_id)
    
    response = [create_response(reservation) for reservation in reservations]

    return response

def submit_reservation(token:Token, reservation:ReservationSchemas.AddReservation, db_session:Session) -> ReservationSchemas.Reservation:
    """
    This function creates a reservation objects in the database based on the reservation provided and validates the inputs
        Requires:
            access_token: JWTToken generated at login
            reservation: Reservation data based on the AddReservation schema
            db_session: A database session that provides access to the database
        The service duration has to fit the length of the appointment, the appointemt needs to be in the future, 
        the appointent cannot already be reseved, the service has to be found in the database
    """
    user = verify_user(db_session=db_session, access_token=token.access_token, return_user=True)

    appointment = db_appointment.get_appointent_by_id(db=db_session, appointment_id=reservation.appointment_id)
    if  appointment == None:
        raise HTTPException(status_code=404, detail="Appointment with this id is not found")
    if appointment.starts < datetime.now():
        raise HTTPException(status_code=406, detail="The appointment is already passed")
    #Validating the appointment it checks if it exist or it is passed

    if appointment.status == "reserved":
        raise HTTPException(status_code=409, detail="The appointment is already reserved")
    #Checking for the status of the appointment

    service = db_service.get_service_by_id(db=db_session, service_id=reservation.reservation_data.id)

    if service == None:
        raise HTTPException(status_code=404, detail="Service with this id is not found")
    #Checking if service exist

    if service.name != reservation.reservation_data.name or service.description != reservation.reservation_data.description or service.service_type != reservation.reservation_data.service_type or service.lenght != reservation.reservation_data.lenght or service.comment != reservation.reservation_data.comment or service.price != reservation.reservation_data.price:
        raise HTTPException(status_code=406, detail="Not valid service")
    #Checking if the service submitted is the same with the one in the database
    
    if service.lenght > ((appointment.ends - appointment.starts).total_seconds()/60):
        raise HTTPException(status_code=406, detail="Service takes longer than the appointment")
    #Checking if the appointment is long enough for the service reserved

    db_item = db_reservation.add_reservation(
        db=db_session,
        appointent_id=reservation.appointment_id,
        reservation_data=reservation.reservation_data.dict(),
        user_id=user.id,
    )

    db_appointment.update_appointent_status(db=db_session, appointment_id=db_item.appointment_id, status="reserved")
    
    return create_response(db_item=db_item)

def delete_reservation(token:Token, reservation_id:int, db_session:Session):
    """
    This fucntion returns the reservations connected to the user with the userid provided
        Requires:
            access_token: JWTToken generated at login
            reservation_id: The the id of the reservation for deleting
            db_session: A database session that provides access to the database
    """
    user = verify_user(db_session=db_session, access_token=token.access_token, return_user=True)

    reservation = db_reservation.get_reservation_by_id(db=db_session, reservation_id=reservation_id)

    if reservation == None:
        raise HTTPException(status_code=404, detail="Reservation with this id does not found")
    #Checking if the reservation exists
    if reservation.user_id != user.id and user.access_level != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized to access this request")
    #Checking if the user requesting has access to the reservaion

    appointent = db_appointment.get_appointent_by_id(db=db_session, appointment_id=reservation.appointment_id)

    db_reservation.delete_reservation(db=db_session, reservation_id=reservation_id)
    db_appointment.update_appointent_status(db=db_session, appointment_id=appointent.id, status="free")
