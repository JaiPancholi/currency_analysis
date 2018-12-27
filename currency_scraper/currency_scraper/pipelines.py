# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import SpotRate

engine = create_engine(os.getenv('DB_URL'), echo=True)
Session = sessionmaker(bind=engine)

class BankScraperPipeline(object):
    def process_item(self, item, spider):
        session = Session()
        sr = SpotRate(
            url=item['url'],
            day=item['day'],
            month=item['month'],
            year=item['year'],
            base_currency=item['base_currency'],
            target_currency=item['target_currency'],
            base_value=item['base_value'],
            target_spot_rate=item['target_spot_rate'],
            target_52wk_high=item['target_52wk_high'],
            target_52wk_low=item['target_52wk_low']
        )

        session.add(sr)
        session.commit()
        return item