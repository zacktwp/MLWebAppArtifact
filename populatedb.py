from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Iris, Base, User
import datetime

datetime_object = datetime.datetime.now()

engine = create_engine('sqlite:///iris.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(name="zack peterson", email="zacktwp@gmail.com")

session.add(user1)
session.commit()

Iris1 = Iris(created_date=datetime_object,
                    sepallength="0",
                    sepalwidth="0",
                    petallength="0",
                    petalwidth="0")

session.add(Iris1)
session.commit()

print ("added Polution to DB!")
