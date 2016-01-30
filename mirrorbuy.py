import re
import json
import moira
import requests
import os
from moira import moira
from bs4 import BeautifulSoup
import trans as t

t.getHistory("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2015/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")


username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'meisenheimer'

#Set filename
filename = "history.txt"
#Instantiate mynet
mynet = 0
#Log in to marketwatch
token = moira.get_token(username, password)
#Try to get user portfolio, if not, assume it is 1000000
try:
    portfolio = moira.get_portfolio_data(token, game)
    #Get net worth from portfolio
    mynet = portfolio["net_worth"]
except:
    mynet = 1000000.00

symbols = t.getSymbols()
orderdate = t.getOrderdate()
transdate = t.getTransdate()
ordertype = t.getOrdertype()
orderamount = t.getOrderamount()
orderprice = t.getOrderprice()
allitems = []

def writeData():
    print "Begin append"
    for item in symbols:
        print "Appending symbol"
        allitems.append(item)
    for item in orderdate:
        print "Appending orderdate"
        allitems.append(item)
    for item in transdate:
        print "Appending transdate"
        allitems.append(item)
    for item in ordertype:
        print "Appending ordertype"
        allitems.append(item)
    for item in orderamount:
        print "Appending orderamount"
        allitems.append(item)
    for item in orderprice:
        print "Appending orderprice"
        allitems.append(item)

    print "Begin writing"
    text_file = open(filename, "w")
    for item in allitems:
        text_file.write(str(item) + "\n")
    text_file.close()

def readData():
    fileout = []
    readsymbols = []
    readorderdate = []
    readtransdate = []
    readordertype = []
    readorderamount = []
    readorderprice = []
    print 'Begin read'
    f = open(filename)
    for line in iter(f):
        fileout.append(line)
    f.close()
    print len(fileout)
    print fileout[0]
    print fileout[1]
    print fileout
    for item in range(0, len(fileout)):
        for x in range(0, len(fileout), 5):
            readsymbols = fileout[x]
        for x in range(1, len(fileout), 5):
            readrderdate = fileout[x]
        for x in range(2, len(fileout), 5):
            readtransdate = fileout[x]
        for x in range(3, len(fileout), 5):
            readordertype = fileout[x]
        for x in range(4, len(fileout), 5):
            readorderamount = fileout[x]
        for x in range(5, len(fileout), 5):
            readorderprice = fileout[x]
    print 'readsymbols'
    for item in readsymbols:
        print item
    print 'readorderdate'
    for item in readorderdate:
        print item
    print 'readtransdate'
    for item in readtransdate:
        print item
    print 'readordertype'
    for item in readordertype:
        print item
    print 'readorderamount'
    for item in readorderamount:
        print item
    print 'readorderprice'
    for item in readorderprice:
        print item

#Check if file exists, if not, create one
if not os.path.isfile(filename):
    print "File not found, creating file"
    open(filename, 'w').close()

#Check if file is empty
if os.stat(filename).st_size == 0:
    print "File empty, writing base information"
    writeData()

readData()



"""
hisnet = 295988.97
price = 7.45
shares_he_bought = 2022
print price * (mynet / hisnet) * shares_he_bought
"""
