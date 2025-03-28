from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Date, Boolean, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    city = Column(String)
    mail = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    salt = Column(LargeBinary)

    events = relationship("DataEvent", back_populates="owner")

class DataEvent (Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    event_date = Column(Date)
    event_time = Column(Time)
    name = Column(String)
    description = Column(String, nullable=True)
    category = Column(Boolean)

    owner = relationship("DataUser", back_populates="events")