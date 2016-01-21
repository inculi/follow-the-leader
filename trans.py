import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup
from googlefinance import getQuotes

url = "http://www.marketwatch.com/game/stock-fears/portfolio/transactionhistory?name=Dustin%20Lien&p=1354179"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

tickers = soup.find_all("td")

for item in tickers:
    print item.text.replace("\t", "").replace("\r", "").replace("\n", "")
