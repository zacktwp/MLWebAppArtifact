import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class Iris(Base):
    __tablename__ = 'iris'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    #name = Column(String(250), nullable=False)
    sepallength = Column(String(8))
    sepalwidth = Column(String(8))
    petallength = Column(String(8))
    petalwidth = Column(String(8))



engine = create_engine('sqlite:///iris.db')


Base.metadata.create_all(engine)
