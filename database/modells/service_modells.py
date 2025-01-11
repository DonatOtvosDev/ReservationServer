from sqlalchemy import Column, Integer, String

from reps.database_reps.database import Base

class Service(Base):
    """
    This is the orm modell of the services
        id: The primary and unique identifier of a service
        name: The name of the reservation
        description: A short summary of what is the service about
        commnet: Additional infromation to the price
        price: The price of the service
        lenght: The duration of the appointment
    """
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    service_type = Column(String)
    description = Column(String)
    comment = Column(String)
    price = Column(Integer)
    lenght = Column(Integer)