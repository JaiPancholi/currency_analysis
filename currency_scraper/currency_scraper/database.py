import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
	import models
	from models import SpotRate
except ModuleNotFoundError:
	from currency_scraper import models
	from currency_scraper.models import SpotRate

def create_tables():
	engine = create_engine(os.getenv('DB_URL'), echo=True)
	Base.metadata.create_all(engine)

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
	urls = set()
	for row in rows:
		urls.add(row[0])
	return urls


if __name__ == '__main__':
	retrieve_scraped_urls()