from fastapi import APIRouter, Depends, UploadFile, File, Header
from sqlalchemy.orm import Session
from reps.database_reps.database_services import get_db

import database.schemas.AuthSchemas as AuthSchemas
import database.schemas.PagesSchemas as PagesSchemas

import reps.standad_reps.pagesReps as pagesReps

router = APIRouter()

@router.get("/homescreen", tags=["Pages"], response_model=PagesSchemas.HomeScreenData ,status_code=200)
async def get_home_screen(db:Session = Depends(get_db)):
    return pagesReps.get_home_screen(db_session=db)

@router.post("/homescreen/update", tags=["Pages"], status_code=202)
async def update_home_screen(token:AuthSchemas.Token, data:PagesSchemas.DataToUpdate, db:Session=Depends(get_db)):
    return pagesReps.edit_home_screen(token=token, data=data, db_session=db)

@router.get("/homescreen/picture", tags=["Pages"])
async def show_hom_screen_pic(db:Session=Depends(get_db)):
    return pagesReps.get_home_screen_pic(db_session=db)

@router.post("/homescreen/picture", tags=["Pages"])
async def update_home_screen_pic(file: UploadFile = File(), db:Session = Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return await pagesReps.upload_image_home_screen(access_token=token, file=file, db_session=db)

@router.get("/aboutmescreen",response_model=PagesSchemas.AboutMeScreenData ,tags=["Pages"], status_code=200)
async def get_about_me_screen(db:Session = Depends(get_db)):
    return pagesReps.get_aboutmescreen(db_session=db)

@router.post("/aboutmescreen/update", tags=["Pages"], status_code=202)
async def update_home_screen(token:AuthSchemas.Token, data:PagesSchemas.DataToUpdate, db:Session=Depends(get_db)):
    return pagesReps.edit_aboutme_screen(token=token, data=data, db_session=db)

@router.get("/aboutmescreen/picture", tags=["Pages"])
async def show_aboutme_screen_pic(db:Session=Depends(get_db)):
    return pagesReps.get_aboutme_screen_pic(db_session=db)

@router.post("/aboutmescreen/picture", tags=["Pages"])
async def update_aboutme_screen_pic(file: UploadFile = File(), db:Session = Depends(get_db),
        token: str = Header(), token_type: str = Header(default=None)):
    return await pagesReps.upload_image_aboutme_screen(access_token=token, file=file, db_session=db)