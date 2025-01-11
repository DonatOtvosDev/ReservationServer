from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from reps.database_reps.database_services import get_db

import database.schemas.AuthSchemas as AuthSchemas
import database.schemas.UserSchemas as UserSchemas

import reps.standad_reps.userReps as userReps

router = APIRouter()

@router.post("/token", response_model=AuthSchemas.TokenWithAccesLevel, tags=["User"], status_code=201)
async def sing_user_in(user:UserSchemas.LoginUser, db:Session = Depends(get_db)):
    return userReps.authenticate_user(user=user, db_session=db)

@router.post("/sign_up", response_model=UserSchemas.User, tags=["User"], status_code=201)
async def sign_user_up(user:UserSchemas.CreateUser, db:Session = Depends(get_db)):
    return userReps.create_user(user=user, db_session=db)

@router.get("/me", response_model=UserSchemas.User, tags=["User"], status_code=200)
async def get_user(db:Session=Depends(get_db),
token: str = Header(), token_type: str = Header(default=None)):
    return userReps.get_user(access_token=token, db_session=db)

@router.post("/user/changepasword", tags=["User"], status_code=202)
async def change_password(token: AuthSchemas.Token, user:UserSchemas.ChangePassword, db:Session = Depends(get_db)):
    return userReps.change_passrowd(token=token, user=user, db_session=db)

@router.post("/user/update",response_model=UserSchemas.User, tags=["User"], status_code=202)
async def update_user(token:AuthSchemas.Token, user:UserSchemas.ChangeUserInfo, db:Session = Depends(get_db)):
    return userReps.update_user_data(token=token, user=user, db_session=db)

@router.get("/users", response_model=list[UserSchemas.UserItem], tags=["User"], status_code=200)
async def get_users(limit:int = 10, skip:int=0, filter:str=None, db:Session=Depends(get_db),
token: str = Header(), token_type: str = Header(default=None)):
    return userReps.get_users(access_token=token, limit=limit, skip=skip, filter=filter, db_session=db)

@router.get("/users/pending", response_model=list, tags=["User"], status_code=200)
async def pending_users(limit:int = 10, skip:int=0, db:Session=Depends(get_db),
token: str = Header(), token_type: str = Header(default=None)):
    return userReps.get_users_pending(access_token=token, limit=limit, skip=skip, db_session=db)

@router.post("/user/add", tags=["User"], status_code=202)
async def give_access(token:AuthSchemas.Token, user:UserSchemas.UserAdd, db:Session = Depends(get_db)):
    return userReps.allow_user(token=token, user_id=user.id, db_session=db)

@router.post("/user/ban", tags=["User"], status_code=202)
async def forbid_access(token:AuthSchemas.Token, user:UserSchemas.UserAdd, db:Session = Depends(get_db)):
    return userReps.ban_user(token=token, user_id=user.id, db_session=db)

@router.delete("/user/deleteinfo", tags=["User"], status_code=202)
async def delete_user(token:AuthSchemas.Token, user:UserSchemas.LoginUser, db:Session = Depends(get_db)):
    return userReps.whitdrawdata(token=token, user_info=user, db_session=db)