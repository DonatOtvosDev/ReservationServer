from sqlalchemy import Column, Integer, String

from reps.database_reps.database import Base

class DataPiece(Base):
    """
    This is the orm modell of the dataentries on the home screen
        id: The primary identifier of the key
        key: The key of the data
        content: The content
        screen_name: The name of the screen
    """
    __tablename__ = "screendata"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    content = Column(String)
    screen_name = Column(String)