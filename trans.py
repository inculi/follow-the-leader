import requests
import pandas as pd
from moira import moira
import mmutils as mm
from bs4 import BeautifulSoup

def getTrans(inputUrl):
    #Output
    symbols = []
    orderdate = []
    transdate = []
    ordertype = []
    orderamount = []
    orderprice = []

    ## BEAUTIFULSOUP SETUP
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

    # Find the person's name
    url = inputUrl
    name = url.rsplit("?name=", 1)[1]
    name = name.rsplit("&p=", 1)[0]
    name = name.replace("%20", " ")
    print name

    # Pandas setup
    orderd = {
        'Stock ticker' : pd.Series(symbols, index=orderdate),
        'Order date' : pd.Series(orderdate, index=orderdate),
        'Transaction Date' : pd.Series(transdate, index=orderdate),
        'Order type' : pd.Series(ordertype, index=orderdate),
        'Order amount' : pd.Series(orderamount, index=orderdate),
        'Order price' : pd.Series(orderprice, index=orderdate)
        }

    orderdf = pd.DataFrame(orderd)
    print orderdf
    orderdf.to_csv(name + " transactions.csv")

# getTrans("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")
