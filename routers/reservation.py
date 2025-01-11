from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from reps.database_reps.database_services import get_db

from database.schemas.AuthSchemas import Token

import reps.standad_reps.reservationReps as reservationReps
import database.schemas.ReservationSchemas as ReservationSchemas



router = APIRouter()

@router.get("/reservations/me",response_model=list[ReservationSchemas.Reservation], tags=["Reservation"], status_code=200)
async def get_reservations(db:Session = Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return reservationReps.get_reservations_user(token=token, db_session=db)

@router.get("/reservations/user",response_model=list[ReservationSchemas.Reservation], tags=["Reservation"], status_code=200)
async def get_reservations(user_id:int, db:Session = Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return reservationReps.get_reservations_admin_by_user(user_id=user_id, token=token, db_session=db)

@router.post("/reservation/create",response_model=ReservationSchemas.Reservation, tags=["Reservation"], status_code=201)
async def create_reservation(token:Token, reservation : ReservationSchemas.AddReservation, db:Session=Depends(get_db)):
    return reservationReps.submit_reservation(token=token, reservation=reservation, db_session=db)

@router.delete("/reservation/delete", tags=["Reservation"], status_code=202)
async def delete_reservation(token:Token, reservation:ReservationSchemas.DeleteReservation, db:Session=Depends(get_db)):
    return reservationReps.delete_reservation(token=token, reservation_id=reservation.reservation_id, db_session=db)