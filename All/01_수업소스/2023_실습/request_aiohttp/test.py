import requests 
from bs4 import BeautifulSoup 
url = "https://www.iban.com/currency-codes"
iban_result = requests.get(url) 
iban_soup = BeautifulSoup(iban_result.text, 'html.parser')
table = iban_soup.table 
trs = table.find_all('tr') 
currency_list=[] 
for idx, tr in enumerate(trs): 
    if idx > 0: 
        tds = tr.find_all('td') 
        country = tds[0].text.strip() 
        currency = tds[1].text.strip() 
        code = tds[2].text.strip() 
        number = tds[3].text.strip() 
        currency_list.append({ "idx":idx, "country": country, "currency": currency, })