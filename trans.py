import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup
from googlefinance import getQuotes

url = "http://www.marketwatch.com/game/stock-fears/portfolio/transactionhistory?name=Dustin%20Lien&p=1354179"
def getHistory(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    tickers = []
    symbols = []
    orderdate = []
    transdate = []
    ordertype = []
    orderamount = []
    orderprice = []

    x = 0

    for item in soup.find_all("td"):
        if item.find(class_='pubDate'):
	        break
        tickers.append(item)

    x = 0
    for item in tickers:
        if item.parent.name == "tr":
            good_text = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
            information = good_text.rstrip().split('\n')

            if x == 0:
                symbols.append(information)
                if x == 1:
                    orderdate.append(information)
                if x == 2:
                    transdate.append(information)
                if x == 3:
                    ordertype.append(information)
                if x == 4:
                    orderamount.append(information)
                if x == 5:
                    orderprice.append(information)
            x += 1
            if x == 6:
                x = 0


    print "Stock ticker"
    for item in symbols:
        print item

    print "Order date"
    for item in orderdate:
        print item

    print "Transaction date"
    for item in transdate:
        print item

    print "Order date"
    for item in ordertype:
        print item

    print "Order amount"
    for item in orderamount:
        print item

    print "Order price"
    for item in orderprice:
        print item
