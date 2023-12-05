from sqlalchemy import Column, Integer, Float, String, Date, create_engine, inspect, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

import Components.config as config

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

inspector = inspect(engine)
if not inspector.has_table('satellites'):
    Base.metadata.create_all(engine)


def commitSatellites(data, obs_latitude, obs_longitude):
    Session = sessionmaker(bind=engine)
    session = Session()

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
    Session = sessionmaker(bind=engine)
    session = Session()

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
        Session = sessionmaker(bind=engine)
        session = Session()

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

def getSatellitesFiltered(satname,satlatitude,satlongitude,sataltitude):
    Session = sessionmaker(bind=engine)
    session = Session()

    satellites = session.query(Satellite).with_entities(Satellite.satid,
                                                        Satellite.satname,
                                                        Satellite.satlatitude,
                                                        Satellite.satlongitude,
                                                        Satellite.sataltitude,
                                                        ).filter_by(satname=satname, 
                                                                    satlatitude=satlatitude, 
                                                                    satlongitude=satlongitude,
                                                                    sataltitude=sataltitude).all()

    satellites_dicts = [dict(zip(['satid', 'satname', 'satlatitude', 'satlongitude', 'sataltitude'], sat)) for sat in satellites]

    session.close()
    return satellites_dicts