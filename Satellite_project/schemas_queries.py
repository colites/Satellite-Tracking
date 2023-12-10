from sqlalchemy import Column, Integer, Float, String, Date, create_engine, inspect, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

import config

##This is mostly for configuring locally
DATABASE_TYPE = 'postgresql'  
USERNAME = config.DB_USER
PASSWORD = config.DB_PASS
HOST = config.DB_HOST
DATABASE_NAME = config.DB_NAME
PORT = '5432'

DATABASE_URI = 'postgresql://colder:FjRRXNPZw3nTLe41wkIpy3oSllHPI9oL@dpg-clq7m89jvg7s73e44kp0-a.oregon-postgres.render.com/satellites_proj_4e0l'

Base = declarative_base()

engine = None
Session = None

## Lazy loading technique for loading database, only load when it is needed
def initializeDatabase():
    global engine, Session
    if not engine:
        engine = create_engine(DATABASE_URI)
        Session = sessionmaker(bind=engine)

    inspector = inspect(engine)

    if not inspector.has_table('satellites'):
        Base.metadata.create_all(engine)

def getSession():
    if not engine or not Session:
        initializeDatabase()
    return Session()

class Satellite(Base):
    __tablename__ = 'satellites'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    observerlatitude =  Column(Float)
    observerlongitude = Column(Float)
    satid = Column(Integer, nullable=False)
    inter_designator = Column(String)
    satname = Column(String)
    launch_date = Column(String)
    satlatitude = Column(Float)
    satlongitude = Column(Float)
    sataltitude = Column(Float)
    
    __table_args__ = (UniqueConstraint('date', 'satid','observerlatitude','observerlongitude'),)


def commitSatellites(data, obs_latitude, obs_longitude):
    session = getSession()

    try:
        for sat_data in data["above"]:
            satellite = Satellite(date=date.today(),
                                observerlatitude=obs_latitude,
                                observerlongitude=obs_longitude,
                                satid=sat_data['satid'],
                                inter_designator=sat_data['intDesignator'],
                                satname=sat_data['satname'],
                                launch_date=sat_data['launchDate'],
                                satlatitude=sat_data['satlat'],
                                satlongitude=sat_data['satlng'],
                                sataltitude=sat_data['satalt'])
            
            session.add(satellite)
            session.commit()

    except IntegrityError:
        session.rollback()
        session.close()
        return "success"
    
    except Exception as e:
        print("Database error:", e)
        session.rollback()
        session.close()
        return "fail"

    session.close()
    return "success"

def getSatellites(latitude, longitude):
    session = getSession()

    satellites = session.query(Satellite).with_entities(Satellite.satid,
                                                        Satellite.satname,
                                                        Satellite.satlatitude,
                                                        Satellite.satlongitude,
                                                        Satellite.sataltitude,
                                                        ).filter_by(observerlatitude=latitude, observerlongitude=longitude).all()

    satellites_dicts = [dict(zip(['satid', 'satname', 'satlatitude', 'satlongitude', 'sataltitude'], sat)) for sat in satellites]

    session.close()
    return satellites_dicts

def getAllSatellites():
    try:
        session = getSession()

        satellites = session.query(Satellite).with_entities(Satellite.satid,
                                                            Satellite.satname,
                                                            Satellite.satlatitude,
                                                            Satellite.satlongitude,
                                                            Satellite.sataltitude,
                                                            ).all()

        satellites_dicts = [dict(zip(['satid', 'satname', 'satlatitude', 'satlongitude', 'sataltitude'], sat)) for sat in satellites]

    except Exception as e:
        print("Database error:", e)
        session.close()
        return "fail"

    session.close()
    return satellites_dicts

def getSatellitesFiltered(satname="", satlatitude="", satlongitude="", sataltitude=""):
    session = getSession()

    satellites = session.query(Satellite).with_entities(Satellite.satid,
                                                        Satellite.satname,
                                                        Satellite.satlatitude,
                                                        Satellite.satlongitude,
                                                        Satellite.sataltitude,
                                                        )

    if satname:
        satellites = satellites.filter(Satellite.satname == satname)
    if satlatitude:
        satellites = satellites.filter(Satellite.satlatitude == satlatitude)
    if satlongitude:
        satellites = satellites.filter(Satellite.satlongitude == satlongitude)
    if sataltitude:
        satellites = satellites.filter(Satellite.sataltitude == sataltitude)
    
    satellites = satellites.all()
    
    satellites_dicts = [dict(zip(['satid', 'satname', 'satlatitude', 'satlongitude', 'sataltitude'], sat)) for sat in satellites]

    session.close()
    return satellites_dicts
