import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://bhart@localhost/postgres')

db = scoped_session(sessionmaker(engine))

flights = db.execute("SELECT origin, dest, depart_time, duration FROM flights").fetchall()

for flight in flights:
    print(f"{flight.origin} -> {flight.dest}: {flight.duration}")
    