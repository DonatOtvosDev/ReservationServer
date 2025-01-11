from reps.database_reps.database import SessionLocal, engine 
import database.modells.calendar_modells as models

def create_db():
    """
    This functiomn generates a database with the use of SQLAlchemy
    """
    models.Base.metadata.create_all(bind=engine)

def get_db():
    """
    This function creates a database session that allows communication with it.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
