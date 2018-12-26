# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CurrencyScraperItem(scrapy.Item):
    url = scrapy.Field()
    day = scrapy.Field()
    month = scrapy.Field()
    year = scrapy.Field()
    base_currency = scrapy.Field()
    target_currency = scrapy.Field()
    base_value = scrapy.Field()
    target_spot_rate = scrapy.Field()
    target_52wk_high = scrapy.Field()
    target_52wk_low = scrapy.Field()