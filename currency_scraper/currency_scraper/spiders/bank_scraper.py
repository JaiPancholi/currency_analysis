# -*- coding: utf-8 -*-
import scrapy
from currency_scraper.items import CurrencyScraperItem
import re
import calendar


class BankScraper(scrapy.Spider):
    name = 'bank_scraper'

    def start_requests(self):
        start_urls = ['https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD=21&TM=Dec&TY=2018&into=GBP&rateview=D']
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for el in response.xpath('//*[@id="editorial"]/table/tr'):
            day, month, year, base_currency = self.parse_url(response.url)
            target_currency = el.xpath('td/a/text()').extract()
            
            row_data = el.xpath('td/text()').extract()
            target_spot_rate = row_data[0].strip()
            target_52wk_high = row_data[1].strip()
            target_52wk_low = row_data[2].strip()

            yield CurrencyScraperItem(
                    day=day,
                    month=month,
                    year=year,
                    base_currency=base_currency,
                    target_currency=target_currency,
                    base_value=1,
                    target_spot_rate=target_spot_rate,
                    target_52wk_high=target_52wk_high,
                    target_52wk_low=target_52wk_low
                )

    def parse_url(self, url):
        matches = re.search('TD=(\d+)&TM=(\w+)&TY=(\d{4})&into=(\w{3})', url)
        return matches.group(1), self.string_month_to_int(matches.group(2)), matches.group(3), matches.group(4)
    
    @staticmethod
    def string_month_to_int(month_string):
        return {v: k for k,v in enumerate(calendar.month_abbr)}[month_string]
    