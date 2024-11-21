#TimescaleDB is running on port 5002 on localhost inside of a docker container.
#Working!

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Force(Base):
    __tablename__ = "force"
    machine_id = Column(String(255), primary_key=True, nullable=False)
    job_id = Column(String(255), primary_key=True, nullable=False)
    time_stamp = Column(DateTime, primary_key=True, nullable=False)
    fx = Column(Float, nullable=False)
    fy = Column(Float, nullable=False)
    fz = Column(Float, nullable=False)

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5002/postgres")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_force_data = Force(
    machine_id="machine_001",
    job_id="job_001",
    time_stamp=datetime.datetime.now(),
    fx=10.12345,
    fy=20.54321,
    fz=30.98765
)
session.add(new_force_data)
session.commit()

# Retrieve and display records from the Force table
retrieved_data = session.query(Force).all()
for data in retrieved_data:
    print(f"Machine_ID: {data.machine_id}, Job_ID: {data.job_id}, Time_Stamp: {data.time_stamp}, "
          f"Fx: {data.fx}, Fy: {data.fy}, Fz: {data.fz}")
