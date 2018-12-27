import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
	import models
	from models import SpotRate
except ModuleNotFoundError:
	from db import models
	from db.models import SpotRate

def add_dummy_data():
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()

	sr = SpotRate(
		url='https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD=21&TM=Dec&TY=2018&into=GBP&rateview=D',
		day=25,
		month=12,
		year=2018,
		base_currency='GBP',
		target_currency='USD',
		base_value=1,
		target_spot_rate='1.52',
		target_52wk_high='1.52',
		target_52wk_low='1.52'
	)

	session.add(sr)
	session.commit()

def retrieve_scraped_urls():
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()
	rows = session.query(SpotRate.url).all()
	# rows = pull_scraped_table()
	urls = set()
	for row in rows:
		urls.add(row[0])
	return urls

def pull_scraped_table():
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()
	rows = session.query(SpotRate).all()
	return rows

def start_session():
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Session = sessionmaker(bind=engine)
	session = Session()
	return session


if __name__ == '__main__':
	# print(len(retrieve_scraped_urls())) # 14850
	# create_tables()
	print(len(pull_scraped_table()[0]))