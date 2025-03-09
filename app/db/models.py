from sqlalchemy import Column, Integer, String, BINARY, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    city = Column(String)
    mail = Column(String, unique=True, index=True)
    password = Column(BINARY)
    salt = Column(BINARY)

    events = relationship("DataEvent", back_populates="owner")

class DataEvent (Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    event_date = Column(DateTime)
    name = Column(String)
    description = Column(String, nullable=True)
    category = Column(String)

    owner = relationship("DataUser", back_populates="events")