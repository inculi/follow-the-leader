import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup

#Output
symbols = []
orderdate = []
transdate = []
ordertype = []
orderamount = []
orderprice = []



def getURLs(url):
    page = 0
    index = url.find('name=')

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    people = soup.find_all("p")
    for item in people:
        if item.parent.name == 'nav':
            re1='.*?'	# Non-greedy match on filler
            re2='\\d+'	# Uninteresting: int
            re3='.*?'	# Non-greedy match on filler
            re4='\\d+'	# Uninteresting: int
            re5='.*?'	# Non-greedy match on filler
            re6='(\\d+)'	# Integer Number 1

            rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
            m = rg.search(item.text)
            if m:
                int1=m.group(1)
                total = int(int1)
            for page in xrange (0,total,10):
                getHistory(url[:index] + 'index=' + str(page) + '&' + url[index:])



def getHistory(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    tickers = []

    x = 0

    for item in soup.findAll('table')[0].tbody.findAll('td'):
        if item.find(class_='highlight condensed'):
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


getURLs("http://www.marketwatch.com/game/stock-fears/portfolio/transactionhistory?name=Dustin%20Lien&p=1354179")

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
