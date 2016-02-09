import requests
import pandas as pd
import mmutils as mm
import os.path
from bs4 import BeautifulSoup

#Output
symbols = []
orderdate = []
transdate = []
ordertype = []
orderamount = []
orderprice = []
name = ""

def getHistory(inputUrl):
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content, "html.parser")

    # Ticker Symbols
    mm.appendData(0,1,symbols,'str', inputUrl)

    # Order Date and Time
    mm.appendData(1,2,orderdate,'str', inputUrl)

    # Transaction Date and Time
    mm.appendData(2,3,transdate,'str', inputUrl)

    # Order Type
    mm.appendData(3,4,ordertype,'str', inputUrl)

    # Order Amount (number of shares)
    mm.appendData(4,5,orderamount,'float', inputUrl)

    # Order Price
    mm.appendData(5,6,orderprice,'money', inputUrl)

    getTrans()

    name = inputUrl.rsplit("?name=", 1)[1]
    name = name.rsplit("&p=", 1)[0]
    name = name.replace("%20", " ")

def getSymbols():
    return symbols
def getOrderdate():
    return orderdate
def getTransdate():
    return transdate
def getOrdertype():
    return ordertype
def getOrderamount():
    return orderamount
def getOrderprice():
    return orderprice

#url = "http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199"
#url = "http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=James%20McGregor&p=1491149"
#getHistory(url)


"""
#Check if file exists, if not, create one
if not os.path.isfile(filename):
    print "File found, deleting file"
    open(filename, 'w').close()
"""

orderd = {
    'name' : pd.Series(name, index=orderdate),
    'symbol' : pd.Series(symbols, index=orderdate),
    'orderdate' : pd.Series(orderdate, index=orderdate),
    'transdate' : pd.Series(transdate, index=orderdate),
    'ordertype' : pd.Series(ordertype, index=orderdate),
    'orderamount' : pd.Series(orderamount, index=orderdate),
    'orderprice' : pd.Series(orderprice, index=orderdate)
    }

def getTrans():
    orderdf = pd.DataFrame(orderd)
    if os.path.isfile('transactions.csv'):
        old = pd.read_csv('transactions.csv')
        new = pd.merge(orderdf, old)
        new.drop_duplicates(['orderdate'], keep='last')
        #print orderdf
        new.to_csv('transactions.csv', headers=False)
    else:
        orderdf.to_csv('transactions.csv', headers=False)
getTrans()
