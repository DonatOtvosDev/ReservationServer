from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import os

from database.schemas.PagesSchemas import DataToUpdate, HomeScreenData, AboutMeScreenData
from database.schemas.AuthSchemas import Token
from reps.standad_reps.userReps import verify_user

import reps.database_reps.db_pages as db_pages

async def save_file(file:UploadFile, path:str):
    """This function saves a file to the given path"""
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
    await file.close()

def get_home_screen(db_session:Session) -> HomeScreenData:
    """
    This function returns the data for the home screen
    """
    db_data = db_pages.return_data(db=db_session, screen="home")
    
    data = {}
    for item in db_data:
        data[item.key] = item.content
    #The info is sorted into a dict

    if len(list(HomeScreenData.__fields__.keys())) != len(list(data.keys())):
        keys = list(HomeScreenData.__fields__.keys())
        for k in data.keys():
            keys.remove(k)
        raise HTTPException(status_code=422, detail=f"The contet is not updated yet {keys} missing")
    #Checking if a key is missing and returning which if yes
    
    return data

def edit_home_screen(token:Token, data:DataToUpdate, db_session:Session):
    """
    This function updates the data at the key given with the new data given
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            data: The key and value to update
            db_session: A database session that provides access to the database
    """
    verify_user(access_token=token.access_token, auth_admin=True, db_session=db_session)
    
    if not data.key in list(HomeScreenData.__fields__.keys()):
        raise HTTPException(status_code=404, detail="This key is not included in the data")
    #Checking if the key exist in the database
    if len(data.content) < 1:
        raise HTTPException(status_code=400, detail="The content cannot be empty string")
    #Checking if the content is valid

    if db_pages.return_entry(db=db_session, screen="home", key=data.key) != None: 
        db_pages.update_entry(db=db_session, screen="home", key=data.key, content=data.content)
    else:
        db_pages.add_entry(db=db_session, screen="home", key=data.key, content=data.content)
    #The data is updated or added to the database if does not already exist
    return "Accepted"

async def upload_image_home_screen(access_token:str, file:UploadFile, db_session:Session):
    """
    This funcion uploads a new picure or changes the old one of the home screen
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            file: File object of the file uploaded
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=access_token, auth_admin=True)

    filename = file.filename.lower().replace(" ", "_")
    #formating the file name

    if not filename.endswith(('.png', '.jpg', '.jpeg',)):
        raise HTTPException(status_code=415, detail="The file is not an image [png, jpg, jpeg]")
    #validating the picture type

    old_filename_obj = db_pages.return_entry(db=db_session, screen="img", key="homescreenpic")

    if old_filename_obj == None:
        db_pages.add_entry(db=db_session, screen="img", key="homescreenpic", content=filename)
    else:
        os.remove(f"./database/files/{old_filename_obj.content}")
        db_pages.update_entry(db=db_session, screen="img", key="homescreenpic", content=filename)
    #updating the name of the file in db and deleting old pic

    await save_file(file=file, path=f"./database/files/{filename}")    
    #saving the file
    return "Accepted"

def get_home_screen_pic(db_session:Session):
    """This function returns the home screen picture uploaded to the server"""
    filename_obj = db_pages.return_entry(db=db_session, screen="img", key="homescreenpic")
    if filename_obj == None:
        raise HTTPException(status_code=404, detail="Picture is not yet uploaded")
    #Checks if there is a saved path or not
    
    path = f"./database/files/{filename_obj.content}"
    
    if not os.path.isfile(path=path):
        raise HTTPException(status_code=404, detail="The path to the file does not exist")
    #Checks if the file exists or not

    return FileResponse(path=path)

def get_aboutmescreen(db_session:Session) -> AboutMeScreenData:
    """
    This function returns the data for the about me screen
    """
    db_data = db_pages.return_data(db=db_session, screen="aboutme")
    
    data = {}
    for item in db_data:
        data[item.key] = item.content
    #The info is sorted into a dict
    
    if len(list(AboutMeScreenData.__fields__.keys())) != len(list(data.keys())):
        keys = list(AboutMeScreenData.__fields__.keys())
        for k in data.keys():
            keys.remove(k)
        raise HTTPException(status_code=422, detail=f"The contet is not updated yet {keys} missing")
    #Checking if a key is missing and returning which if yes
    
    return data

def edit_aboutme_screen(token:Token, data:DataToUpdate, db_session:Session):
    """
    This function updates the data at the key given with the new data given
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            data: The key and value to update
            db_session: A database session that provides access to the database
    """
    verify_user(access_token=token.access_token, auth_admin=True, db_session=db_session)
    
    if not data.key in list(AboutMeScreenData.__fields__.keys()):
        raise HTTPException(status_code=404, detail="This key is not included in the data")
    #Checking if the key exist in the database
    if len(data.content) < 1:
        raise HTTPException(status_code=400, detail="The content cannot be empty string")
    #Checking if the content is valid

    if db_pages.return_entry(db=db_session, screen="aboutme", key=data.key) != None: 
        db_pages.update_entry(db=db_session, screen="aboutme", key=data.key, content=data.content)
    else:
        db_pages.add_entry(db=db_session, screen="aboutme", key=data.key, content=data.content)
    #The data is updated or added to the database if does not already exist
    return "Accepted"

async def upload_image_aboutme_screen(access_token:str, file:UploadFile, db_session:Session):
    """
    This funcion uploads a new picure or changes the old one of the about me screen
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            file: File object of the file uploaded
            db_session: A database session that provides access to the database
    """
    verify_user(db_session=db_session, access_token=access_token, auth_admin=True)

    filename = file.filename.lower().replace(" ", "_")
    #formating the file name

    if not filename.endswith(('.png', '.jpg', '.jpeg',)):
        raise HTTPException(status_code=415, detail="The file is not an image [png, jpg, jpeg]")
    #validating the picture type

    old_filename_obj = db_pages.return_entry(db=db_session, screen="img", key="aboutmescreenpic")

    if old_filename_obj == None:
        db_pages.add_entry(db=db_session, screen="img", key="aboutmescreenpic", content=filename)
    else:
        os.remove(f"./database/files/{old_filename_obj.content}")
        db_pages.update_entry(db=db_session, screen="img", key="aboutmescreenpic", content=filename)
    #updating the name of the file in db and deleting old pic

    await save_file(file=file, path=f"./database/files/{filename}")    
    #saving the file
    return "Accepted"

def get_aboutme_screen_pic(db_session:Session):
    """This function returns the home screen picture uploaded to the server"""
    filename_obj = db_pages.return_entry(db=db_session, screen="img", key="aboutmescreenpic")
    if filename_obj == None:
        raise HTTPException(status_code=404, detail="Picture is not yet uploaded")
    #Checks if there is a saved path or not

    path = f"./database/files/{filename_obj.content}"
    
    if not os.path.isfile(path=path):
        raise HTTPException(status_code=404, detail="The path to the file does not exist")
    #Checks if the file exists or not

    return FileResponse(path=path)