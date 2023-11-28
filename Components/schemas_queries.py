from sqlalchemy import Column, Integer, Float, String, Date, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

import config

DATABASE_TYPE = 'postgresql'  
USERNAME = config.DB_USER
PASSWORD = config.DB_PASS
HOST = config.DB_HOST
DATABASE_NAME = config.DB_NAME
PORT = '5432'

DATABASE_URI = f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
engine = create_engine(DATABASE_URI)

Base = declarative_base()


class Satellite(Base):
    __tablename__ = 'satellites'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    satid = Column(Integer, nullable=False)
    inter_designator = Column(String)
    satname = Column(String)
    launch_date = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)


inspector = inspect(engine)
if not inspector.has_table('satellites'):
    Base.metadata.create_all(engine)


def commitSatellites(data):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for sat_data in data["above"]:
            satellite = Satellite(date=date.today(),
                                satid=sat_data['satid'],
                                inter_designator=sat_data['intDesignator'],
                                satname=sat_data['satname'],
                                launch_date=sat_data['launchDate'],
                                latitude=sat_data['satlat'],
                                longitude=sat_data['satlng'],
                                altitude=sat_data['satalt'])
            session.add(satellite)
    except Exception as e:
        print("error", e)
        session.close()
        return f"fail"

    session.commit()
    session.close()
    return f"success"