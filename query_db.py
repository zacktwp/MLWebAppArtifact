from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Polution, User

#engine = create_engine('sqlite:///polution.db')
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Below written queries have to be run by copping them into the git bash
# Query first Category name
first = session.query(Polution).order_by(Polution.created_date.desc()).first()
print(first.created_date)
print(first.dew)


# Query all the Dishes in the database
#item = session.query(Polution).all()
#for item in items:
	#print(item.created_date)
	#print(item.name)
