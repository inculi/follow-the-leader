import re
import json
import moira
import requests
import pandas as pd
from moira import moira
import mmutils as mm
from bs4 import BeautifulSoup

#Output
symbols = []
orderdate = []
transdate = []
ordertype = []
orderamount = []
orderprice = []

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

getHistory("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")

orderd = {
    'Order date' : pd.Series(orderdate, index=orderdate),
    'Transaction Date' : pd.Series(transdate, index=orderdate),
    'Stock ticker' : pd.Series(symbols, index=orderdate),
    'Order type' : pd.Series(ordertype, index=orderdate),
    'Order amount' : pd.Series(orderamount, index=orderdate),
    'Order price' : pd.Series(orderprice, index=orderdate)
    }

orderdf = pd.DataFrame(orderd)
print orderdf
# orderdf.to_csv("dataframe2.csv")
