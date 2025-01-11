from sqlalchemy.orm import Session

import database.modells.pages_modells as models

def return_data(db:Session, screen:str) -> list[models.DataPiece]:
    """This function returns the data conencted to the given screen"""
    return db.query(models.DataPiece).filter(models.DataPiece.screen_name == screen).all()

def return_entry(db:Session, screen:str, key:str) -> models.DataPiece | None:
    """This function returns the data entry with the key from the screen"""
    return db.query(models.DataPiece).filter(models.DataPiece.screen_name == screen).filter(models.DataPiece.key == key).first()

def update_entry(db:Session,screen:str, key:str, content:str):
    """This function updates the data entry"""
    db.query(models.DataPiece).filter(models.DataPiece.screen_name == screen).filter(models.DataPiece.key == key).update({"content":content}, synchronize_session=False)
    db.commit()

def add_entry(db:Session, screen:str, key:str, content:str):
    """This function adds the data entry"""
    db_entry= models.DataPiece(
        key = key,
        content = content,
        screen_name = screen
    )
    db.add(db_entry)
    db.commit()