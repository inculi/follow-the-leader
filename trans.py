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
tickers = []

for item in soup.find_all("td"):
    if item.find(class_='pubDate'):
	break
    tickers.append(item)

for item in tickers:
    if item.parent.name == "tr":
        print item.text.replace("\t", "").replace("\r", "").replace("\n", "")
