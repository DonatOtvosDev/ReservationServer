from sqlalchemy.orm import Session

import database.modells.user_modell as models

def get_users(db:Session, skip:int, limit:int, filter:str) -> list[models.User]:
    """
    This function returns and filters if porvided, the users at the offset with the given limit form the database under db session
    """
    if filter != None:
        return db.query(models.User).filter(models.User.access_level == filter).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db:Session, user_id:int) -> models.User:
    """
    This function retruns the user with the given id from the database under db session
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_email_by_email(db:Session, email:str) -> models.User:
    """
    This function retruns the user with the given email address from the database under db session
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db:Session, username:str) -> models.User:
    """
    This function retruns the user with the given username from the database under db session
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_users_pending(db:Session, limit:int, skip:int) -> list[models.User]:
    return db.query(models.User).filter(models.User.access_level == "none").offset(skip).limit(limit).all()

def change_user_access_level(db:Session, user_id:int, new_access_level:str):
    """
    This function updates the user's access_level [user, admin, banneduser] with the given id in the database under db session
    """
    db.query(models.User).filter(models.User.id == user_id).update({"access_level": new_access_level})
    db.commit()

def change_user_password(db:Session, user_id:int, new_hashed_password):
    """
    This function changes the password of the user with the given id in the database under db session
    """
    db.query(models.User).filter(models.User.id == user_id).update({"password": new_hashed_password})
    db.commit()

def update_user(db:Session, user_id:int, data_to_update:dict):
    """
    This function updates the attributes of the user with the given id with data_to_update in the database under db session
    """
    db.query(models.User).filter(models.User.id == user_id).update(data_to_update)
    db.commit()

def create_user(db:Session, user:dict) -> models.User:
    """
    This function creates an user from the data provided in the database under db session
        user: dictionary with the data [username, password, email, phone_number, first_name, sir_name]
    """
    db_user = models.User(
        username = user["username"],
        password = user["password"],
        email = user["email"],
        phone_number = user["phone_number"],
        first_name = user["first_name"],
        sir_name = user["sir_name"]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db:Session, user_id:int):
    """
    This function deletes the user with the given id from the database under db session
    """
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()