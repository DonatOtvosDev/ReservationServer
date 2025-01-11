from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import re

from database.schemas.UserSchemas import CreateUser, LoginUser, ChangePassword, ChangeUserInfo, User, UserItem
from database.schemas.AuthSchemas import Token, TokenWithAccesLevel

from reps.standad_reps.authReps import verify_password, hash_password, create_access_token, return_token_content
import reps.database_reps.db_user as db_user
import reps.database_reps.db_reservation as db_reservations
import reps.database_reps.db_appointment as db_appointment

CREDENTIAL_EXEPTION = HTTPException(status_code=401, detail="Could not validate the credential")


def get_users(access_token:str, limit:int, skip:int, filter:str, db_session:Session) -> list[UserItem]:
    """
    This function returns the users corresponding to the filter
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            limit: The max lengt of the list returned
            skip: The appintents skipped before selecting the list returned
            filter: A filter corresponding to the access level filtered
            db_session: A database session that provides access to the database
    """

    verify_user(db_session=db_session, access_token=access_token, auth_admin=True)
    if filter != "user" and filter != "banneduser" and filter != "admin" and filter != None:
        raise HTTPException(status_code=400, detail="This filter is unavailable!")
    #Checking it the filter is valid access level or there is no filter else raising an error

    users = db_user.get_users(db=db_session, skip=skip, limit=limit, filter=filter)
    users_out = []

    for db_item in users:
        users_out.append({
        "id" : db_item.id,
        "username" : db_item.username,
        "email" : db_item.email,
        "phone_number" : db_item.phone_number,
        "first_name" : db_item.first_name,
        "sir_name" : db_item.sir_name,
        "access_level" : db_item.access_level
        })
    #Adding the users to the response

    return users_out

def get_user(access_token:str, db_session:Session) -> User:
    """
    This function returns the user data of the owner of the token
        Requires:
            access_token: JWTToken generated at login 
            db_session: A database session that provides access to the database
    """
    user = verify_user(db_session=db_session, access_token=access_token, return_user=True)
    
    response = {
        "id" : user.id,
        "username" : user.username,
        "email" : user.email,
        "phone_number" : user.phone_number,
        "first_name" : user.first_name,
        "sir_name" : user.sir_name
    }

    return response

def create_user(user:CreateUser, db_session:Session) -> User:
    """
    This function creates a user in the database
        Requires:
            user: User data based on the CreateUser
            db_session: A database session that provides access to the database
    The data has to be valid string and use only the characters standard for the purpose and use normal email form
    """

    if len(re.findall(pattern="[^a-z0-9]", string=user.username)) > 0 or len(user.username) < 4:
        raise HTTPException(status_code=406, detail="Username is not acceptable")
    if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=user.first_name)):
        raise HTTPException(status_code=406, detail="First name is not acceptable")
    if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=user.sir_name)):
        raise HTTPException(status_code=406, detail="Second name is not acceptable")
    if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=user.email) == None:
        raise HTTPException(status_code=406, detail="Invalid email adress")
    if re.fullmatch(pattern="\d+", string=user.phone_number) == None:
        raise HTTPException(status_code=406, detail="Invalid phone number")
    if len(user.password) < 6:
        raise HTTPException(status_code=406, detail="Password is too short")
    #Validates the input with regex

    if db_user.get_email_by_email(db=db_session, email=user.email) != None:
        raise HTTPException(status_code=409, detail="User with this email already exist")
    if db_user.get_user_by_username(db=db_session, username=user.username) != None:
        raise HTTPException(status_code=409, detail="Username is alredy in use")
    #Checks if the username or email adress is already registered


    

    db_item = db_user.create_user(db=db_session, user={
        "username" : user.username,
        "password" : hash_password(user.password),
        "email" : user.email,
        "phone_number" : user.phone_number,
        "first_name" : user.first_name,
        "sir_name" : user.sir_name
    })

    response = {
        "id" : db_item.id,
        "username" : db_item.username,
        "email" : db_item.email,
        "phone_number" : db_item.phone_number,
        "first_name" : db_item.first_name,
        "sir_name" : db_item.sir_name
    }
    #Creates a response based on the newly generated database item
    return response

def update_user_data(token:Token, user:ChangeUserInfo, db_session:Session) -> User:
    """
    This function updates the user with the data provided
        Requires:
            access_token: JWTToken generated at login
            user: Data to update  in the form of ChangeUserInfo schema at least one new user attribute
            db_session: A database session that provides access to the database
    """ 

    database_user = verify_user(db_session=db_session, access_token=token.access_token, return_user=True)
    if verify_password(planin_pasw=user.password, hashed_pasw=database_user.password) == False:
        raise HTTPException(status_code=401, detail="Password is not correct")
    #Checks if the pasword provided is correct
    data_to_update = {}
    
    if user.email != None and database_user.email != user.email:
        if re.fullmatch(pattern="[a-z0-9/.]+@[a-z0-9/]+\.[a-z]+", string=user.email) == None:
            raise HTTPException(status_code=406, detail="Invalid email adress")
        
        if db_user.get_email_by_email(db=db_session, email=user.email) != None:
            raise HTTPException(status_code=409, detail="User with this email already exist")

        data_to_update["email"] = user.email

    if user.first_name != None and database_user.first_name != user.first_name:
        if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=user.first_name)):
            raise HTTPException(status_code=406, detail="First name is not acceptable")

        data_to_update["first_name"] = user.first_name

    if user.sir_name != None and database_user.sir_name != user.sir_name:
        if len(re.findall(pattern="[^a-zA-z0-9áéíóöőúüűÁÉÍÓÖŐÚÜŰ]", string=user.sir_name)):
            raise HTTPException(status_code=406, detail="Sir name is not acceptable")

        data_to_update["sir_name"] = user.sir_name

    if user.phone_number != None and database_user.phone_number != user.phone_number:
        if re.fullmatch(pattern="\d+", string=user.phone_number) == None:
            raise HTTPException(status_code=406, detail="Invalid phone number")
    
        data_to_update["phone_number"] = user.phone_number

    #Adding the new attributes provided to the data to update list and validating it before

    if len(data_to_update.keys()) == 0:
        raise HTTPException(status_code=406, detail="Parameters provided are not enough to update the user")
    #Checking if there something to update

    db_user.update_user(db=db_session, user_id=database_user.id, data_to_update=data_to_update)

    db_item = db_user.get_user_by_id(user_id=database_user.id, db=db_session)

    response = {
        "id" : db_item.id,
        "username" : db_item.username,
        "email" : db_item.email,
        "phone_number" : db_item.phone_number,
        "first_name" : db_item.first_name,
        "sir_name" : db_item.sir_name
    }
    #Creating response based on the newly updated user

    return response 

def get_users_pending(access_token:str, limit:int, skip:int, db_session:Session):
    """
    This function returns the users pending for approval, this is only used until production
    """
    verify_user(db_session=db_session, access_token=access_token, auth_admin=True)
    users = db_user.get_users_pending(db=db_session, limit=limit, skip=skip)
    users_return = []

    for db_item in users:
        users_return.append({
        "id" : db_item.id,
        "username" : db_item.username,
        "email" : db_item.email,
        "phone_number" : db_item.phone_number,
        "first_name" : db_item.first_name,
        "sir_name" : db_item.sir_name
        })

    return users_return


def allow_user(token:Token, user_id:int, db_session:Session):
    """
    This function adds the user "user" access level
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            user_id: The id of the user that needs to be accepted
            db_session: A database session that provides access to the database
    """ 
    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)
    user = db_user.get_user_by_id(user_id=user_id, db=db_session)
    if  user == None:
        raise HTTPException(status_code=404, detail="User not found with this id")
    if user.access_level == "user" or user.access_level == "admin":
        raise HTTPException(status_code=409, detail="User is already accepted")
    #Checking if the user is available or if it arleady has access

    db_user.change_user_access_level(db=db_session, user_id=user_id, new_access_level="user")

def ban_user(token:Token, user_id:int, db_session:Session):
    """
    This function removes the access of a user
        Requires:
            access_token: JWTToken generated at login (ADMIN)
            user_id: The id of the user whos access needs t be removed
            db_session: A database session that provides access to the database
    """ 
    verify_user(db_session=db_session, access_token=token.access_token, auth_admin=True)
    user = db_user.get_user_by_id(user_id=user_id, db=db_session)
    if  user == None:
        raise HTTPException(status_code=404, detail="User not found with this id")
    #Checking if the user exists with the given id

    if user.access_level == "admin":
        raise HTTPException(status_code=401, detail="Admin cannot be banned")
    #Checking if the user is an admin because that it cannot be banned

    db_user.change_user_access_level(db=db_session, user_id=user_id, new_access_level="banneduser")
    
def authenticate_user(user:LoginUser, db_session: Session) -> TokenWithAccesLevel:
    """
    This function creates an access token to a user if the login infromation is correct
        Requires:
            user: User info pasw and username in the form of Login User Schema
            db_session: A database session that provides access to the database
    """
    if len(re.findall(pattern="[^a-z0-9]", string=user.username)) > 0 or len(user.username) < 4:
        raise HTTPException(status_code=406, detail="Username is not acceptable")
    if len(user.password) < 6:
        raise HTTPException(status_code=406, detail="Password is too short")
    #Checking if the data passed in is valid or not

    user_data = db_user.get_user_by_username(username=user.username, db=db_session)
    if user_data == None:
        raise HTTPException(status_code=404, detail="User not found")
    #Checks if the username is in the database

    if verify_password(user.password, user_data.password) == False:
        raise HTTPException(status_code=401, detail="Password is not correct")
    #Checking if the pasword is Correct

    if user_data.access_level == "none":
        raise HTTPException(status_code=401, detail="User is not yet accepted")
    if user_data.access_level == "banneduser":
        raise HTTPException(status_code=401, detail="Your user had been banned")
    if user_data.access_level != "user" and user_data.access_level != "admin":
        raise HTTPException(status_code=401, detail="Your acces level cannot be comprehended")
    #Checking the access level

    resp = create_access_token(user_name=user.username, user_id=user_data.id)
    resp["access_level"] = user_data.access_level
    #Adding the access level to the response

    return resp

def verify_user(db_session:Session, access_token:str, auth_admin:bool = False, return_user:bool = False) -> None|User:
    """
    This function validates the access token and raises exeption if it is not valid
        Requires:
            db_session: A database session that provides access to the database
            access_token: JWTToken generated at login
            auth_adnim: The level of authentication for admins if needed
            return_user: It returns the user from the database if needed
    """

    data = return_token_content(token=access_token)
    if data == "Error":
        raise CREDENTIAL_EXEPTION
    if data.get("expires") == None:
        raise CREDENTIAL_EXEPTION
    #Checks if the content of the token is valid
    if datetime.utcnow() > datetime.strptime(data["expires"], "%Y-%m-%dT%H:%M:%S.%f"):
        raise HTTPException(status_code=401, detail="Token expired")
    #Checks for expiary
    if data.get("user") == None:
        raise CREDENTIAL_EXEPTION
    #Checks for user info
    if data["user"].get("name") == None or data["user"].get("id") == None:
        raise CREDENTIAL_EXEPTION
    #Checks for detailed user info
    
    user = db_user.get_user_by_id(db=db_session, user_id=data["user"]["id"])

    if user == None:
        raise CREDENTIAL_EXEPTION
    if user.username != data["user"]["name"]:
        raise CREDENTIAL_EXEPTION
    if user.access_level != "user" and user.access_level != "admin":
        raise CREDENTIAL_EXEPTION
    #Checks if the data in the token is the equilent to the one stored it the database

    if auth_admin and user.access_level != "admin":    
        raise HTTPException(status_code=401, detail="The user does not have access to this function")
    #Checks if the admin level required and achieved

    if return_user:
        return user
    #Returns the user if needed

def change_password(access_token:str, user:ChangePassword, db_session:Session):
    """
    This function changes the password in the database associated with the user
        Requires: 
            access_token: JWTToken generated at login
            user: The old pasword and new password based on the ChangePassword schema
            db_session: A database session that provides access to the database
    """

    database_user = verify_user(db_session=db_session, access_token=access_token, return_user=True)

    if len(user.new_password) < 6 or len(user.old_password) < 6:
        raise HTTPException(status_code=406, detail="Password is too short")
    #Checks if the passwords are valid passwords

    if verify_password(planin_pasw=user.old_password, hashed_pasw=database_user.password) == False:
        raise HTTPException(status_code=401, detail="Password is not correct")
    #Checks if the password is correct

    db_user.change_user_password(db=db_session, user_id=database_user.id, new_hashed_password=hash_password(user.new_password))


def whithdraw_data(access_token:str, user:LoginUser, db_session:Session):
    """
    This function deletes all the data associated with the user
        Requires:
            access_token: JWTToken generated at login
            user: Login info based on the Login user schema to make sure the user has access
            db_session: A database session that provides access to the database
    """

    database_user = verify_user(db_session=db_session, access_token=access_token, return_user=True)

    if database_user.username != user.username:
        raise HTTPException(status_code=401, detail="Incorrect username")

    if verify_password(planin_pasw=user.password, hashed_pasw=database_user.password) == False:
        raise HTTPException(status_code=401, detail="Password is not correct")
    #Cheking if the password and the username is correct

    reservations = db_reservations.get_reservations_userid(db=db_session, user_id=database_user.id)

    for reservation in reservations:
        appointement = db_appointment.get_appointent_by_id(db=db_session, appointment_id=reservation.appointment_id)
        if appointement.starts < datetime.now():
            db_appointment.update_appointent_status(db=db_session, appointment_id=appointement.id, status="datadeleted")
        else:
            db_appointment.update_appointent_status(db=db_session, appointment_id=appointement.id, status="free")
    #Setting the appointmentstatuses to the newone for all the reservations

    db_reservations.delete_userinfo(db=db_session, user_id=database_user.id)
    db_user.delete_user(db=db_session, user_id=database_user.id)