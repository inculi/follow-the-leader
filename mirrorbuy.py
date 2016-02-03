import moira
import os
from moira import moira
import trans as t
import pandas as pd
import mmutils

toDo = {'symbol' : [], 'orderdate' : [], 'transdate' : [], 'ordertype' : [], 'orderamount' : [], 'orderprice' : []}
username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'meisenheimer'
filename = "transactions.csv"
#Instantiate mynet
mynet = 0
symbols = []
orderdate = []
transdate = []
ordertype = []
orderamount = []
orderprice = []
allitems = []

t.getHistory("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")

#Log in to marketwatch
token = moira.get_token(username, password)
#Try to get user portfolio, if not, assume it is 1000000
try:
    portfolio = moira.get_portfolio_data(token, game)
    #Get net worth from portfolio
    mynet = portfolio["net_worth"]
except:
    mynet = 1000000.00


dic = pd.read_csv(filename).to_dict()


def checkNew(variable):
    if len(dic[variable]) > 10:
        for x in range(0, len(dic[variable] - 10)):
            toDo[variable][x].append(dic[variable][x + 10])
        doTransaction()

def doTransaction():
    if toDo['symbol']:
        for x in range(0, toDo['symbol']):
            #toDo['symbol'][x]
            #toDo['orderamount'][x]
            print 'moira.order(token, ' + game + ', ' + toDo['ordertype'][x] + ', STOCK-XNAS-' + toDo['symbol'][x].upper() + ', ' + float(toDo['orderamount'][x]) + ')'
            #moira.order(token, 'foo', 'Sell', 'STOCK-XNAS-GRPN', 100)
            exit()
        toDo = {'symbol' : [], 'orderdate' : [], 'transdate' : [], 'ordertype' : [], 'orderamount' : [], 'orderprice' : []}
        readData()

def readData():
    t.getTrans()
    for x in range(0, len(dic['symbol'])):
        symbols.append(dic['symbol'][x])
    for x in range(0, len(dic['orderdate'])):
        symbols.append(dic['orderdate'][x])
    for x in range(0, len(dic['transdate'])):
        symbols.append(dic['transdate'][x])
    for x in range(0, len(dic['ordertype'])):
        symbols.append(dic['ordertype'][x])
    for x in range(0, len(dic['orderamount'])):
        symbols.append(dic['orderamount'][x])
    for x in range(0, len(dic['orderprice'])):
        symbols.append(dic['orderprice'][x])

readData()

while True:
    checkNew('symbol')
    checkNew('orderdate')
    checkNew('transdate')
    checkNew('ordertype')
    checkNew('orderamount')
    checkNew('orderprice')
    readData()
    print todo['symbol']

"""
    mmutils.printAll(symbols)
    mmutils.printAll(orderdate)
    mmutils.printAll(transdate)
    mmutils.printAll(ordertype)
    mmutils.printAll(orderamount)
    mmutils.printAll(orderprice)
"""

"""
hisnet = 295988.97
price = 7.45
shares_he_bought = 2022
print price * (mynet / hisnet) * shares_he_bought
"""
