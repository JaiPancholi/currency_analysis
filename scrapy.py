# https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD=21&TM=Dec&TY=2018&into=GBP&rateview=D
import requests
url = 'https://www.bankofengland.co.uk/boeapps/database/Rates.asp?TD=21&TM=Dec&TY=2018&into=GBP&rateview=D'
r = requests.get(url)
print(r.text)