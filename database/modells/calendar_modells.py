from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.orm import relationship

from reps.database_reps.database import Base

class Month(Base):
    """
    This is the orm modell of the month
        id: The primary and unique identifier of a months
        key: The identifier of month it is the combination of the 4 digit year and 2 digit moth number
        month_number: The number of the month in the year
        from_date: The starting date of the moth
        to_date: The last date in the month
        days: The day objects ordered to the month
    """
    __tablename__ = "months"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(Integer)
    month_number = Column(Integer)
    year = Column(Integer)
    month_name = Column(String)
    from_date = Column(String)
    to_date=Column(String)
    days = relationship("Day", back_populates="month")


class Day(Base):
    """
    This is the orm modell of the days
        id: The primary and unique identifier of a day
        date: The date of the day
        working_day: Shows if there is an appointment or not
        day_name: The name of the day in english
        month_id: The id of the month the day is in
        appointments: The appointmnets under the day object
    """
    __tablename__ = "days"
    id = Column(Integer, primary_key=True,index=True)
    date = Column(Date)
    working_day = Column(Boolean, default=False)
    day_name = Column(String)
    month_id = Column(Integer, ForeignKey("months.id"))
    appointments = relationship("Appointment", back_populates="day")

    month = relationship("Month", back_populates="days")