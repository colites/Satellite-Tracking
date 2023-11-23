from sqlalchemy import Column, Integer, String, Date, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import Backend.config as config

DATABASE_TYPE = 'postgresql'  
USERNAME = config.DB_USER
PASSWORD = config.DB_PASS
HOST = config.DB_HOST
DATABASE_NAME = config.DB_NAME
PORT = '5432'

DATABASE_URI = f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
engine = create_engine(DATABASE_URI)

Base = declarative_base()


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    product_name = Column(String, nullable=False)
    review_text = Column(String, nullable=False)
    stars = Column(Integer)


inspector = inspect(engine)
if not inspector.has_table('reviews'):
    Base.metadata.create_all(engine)

def commitReviews(reviews):
    Session = sessionmaker(bind=engine)
    session = Session()

    for review in reviews:
        session.add(review)

    session.commit()
    session.close()


def getProductReviewsQuery(name):
    Session = sessionmaker(bind=engine)
    session = Session()

    reviews = session.query(Review).filter_by(product_name=name).all()
    session.close()

    return reviews