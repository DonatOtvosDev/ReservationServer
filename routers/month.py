from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from reps.database_reps.database_services import get_db

import database.schemas.AuthSchemas as AuthSchemas

import database.schemas.MonthSchemas as MonthSchemas
import reps.standad_reps.monthReps as monthReps


router = APIRouter()

@router.get("/months", response_model=list[MonthSchemas.getMonthsItem], tags=["Month"] ,status_code=200)
async def get_months(limit:int = 6, skip:int = 0, year:int = None, db:Session = Depends(get_db), 
        token: str = Header(), token_type: str = Header(default=None)):
    return monthReps.get_months(token=token, limit=limit, skip=skip, year=year, db_session=db)

@router.get("/month/{id}", response_model=MonthSchemas.getMonthResponse, tags=["Month"])
async def get_month(id:int, return_days:bool = True, db:Session = Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return monthReps.get_month_by_id(token=token, month_id=id,return_days=return_days, db_session=db)

@router.post("/month/get", response_model=MonthSchemas.getMonthResponse, tags=["Month"])
async def month_by_key(token:AuthSchemas.Token, month:MonthSchemas.getMonth, db: Session = Depends(get_db)):
    if month.create_month == True:
        return monthReps.create_month_rep(token=token.access_token, month_num=month.month_number, year=month.year,return_days=month.return_days, db_session=db)
    return monthReps.get_month_by_key(token=token.access_token , month_num=month.month_number, year=month.year,return_days=month.return_days, db_session= db)
