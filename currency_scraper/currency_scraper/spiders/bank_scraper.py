# -*- coding: utf-8 -*-
import scrapy
from datetime import date, timedelta
import re
import calendar

from currency_scraper.items import CurrencyScraperItem
from currency_scraper.database import retrieve_scraped_urls

class BankScraper(scrapy.Spider):
	name = 'bank_scraper'

	def start_requests(self):
		start_urls = self.build_start_urls()
		for url in start_urls:
			yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		for el in response.xpath('//*[@id="editorial"]/table/tr'):
			day, month, year, base_currency = self.parse_url(response.url)
			target_currency = el.xpath('td/a/text()').extract_first()
			
			row_data = el.xpath('td/text()').extract()
			try:
				target_spot_rate = row_data[0].strip()
			except:
				target_spot_rate = None
			try:
				target_52wk_high = row_data[1].strip()
			except:
				target_52wk_high = None
			try:
				target_52wk_low = row_data[2].strip()
			except:
				target_52wk_low = None

			yield CurrencyScraperItem(
					url=response.url,
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
	
	@staticmethod
	def build_start_urls():
		# start_urls = ['https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD=21&TM=Dec&TY=2018&into=GBP&rateview=D']
		start_date = date(2018, 1, 1)
		end_date = date(2018, 12, 21)
		delta = end_date - start_date

		currencies = ['GBP', 'USD', 'EUR']
		urls = set()

		for currency in currencies:
			for i in range(delta.days + 1):
				this_date = end_date - timedelta(i)
				weekno = this_date.weekday()

				if weekno < 5: # if weekday
					day = this_date.day
					month = this_date.strftime("%b")
					year = this_date.year

					url = f'https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD={day}&TM={month}&TY={year}&into={currency}&rateview=D'
					urls.add(url)

		scraped_urls = retrieve_scraped_urls()
		remaining_urls = urls - scraped_urls

		print(f'{len(scraped_urls)} scraped urls. {len(urls)} total urls. {len(remaining_urls)} remaining urls.')

		return list(urls)