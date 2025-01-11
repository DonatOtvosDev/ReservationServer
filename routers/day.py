from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from reps.database_reps.database_services import get_db
from datetime import date

import database.schemas.DaySchemas as DaySchemas

import reps.standad_reps.dayReps as dayReps


router = APIRouter()

@router.get("/day/{id}", response_model=DaySchemas.Day, tags=["Day"], status_code=200)
async def day_get(id:int, db:Session=Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return dayReps.get_day_id(access_token=token, day_id=id, db_session=db)

@router.get("/getday/{date}", response_model=DaySchemas.Day, tags=["Day"], status_code=200)
async def day_by_date(date:date, db:Session=Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return dayReps.get_day_date(access_token=token, date=date, db_session=db)

@router.get("/getworkingdays", response_model=list[DaySchemas.DayBase], tags=["Day"], status_code=200)
async def get_working_days(limit:int = 90, skip: int = 0, db:Session = Depends(get_db),
    token: str = Header(), token_type: str = Header(default=None)):
    return dayReps.get_working_days(access_token=token,limit=limit, skip=skip, db_session=db)