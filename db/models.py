from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), verbose=True)

Base = declarative_base()

class SpotRate(Base):
	__tablename__ = 'spot_rates'
	id = Column(Integer, primary_key=True)
	url = Column(String)
	day = Column(Integer)
	month = Column(Integer)
	year = Column(Integer)
	base_currency = Column(String)
	target_currency = Column(String)
	base_value = Column(Float)
	target_spot_rate = Column(Float)
	target_52wk_high = Column(Float)
	target_52wk_low = Column(Float)
	created_at = Column(DateTime, server_default=func.now())
	updated_at = Column(DateTime, onupdate=func.now())

if __name__ == '__main__':
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Base.metadata.create_all(engine)