import re
import os
import time
import requests
import datetime
import subprocess
from jrtools import *
# import pandas as pd
import mmutils as mm
from moira import moira
from bs4 import BeautifulSoup


debugMode = True # set to true to see current actions

def makeName(inputUrl):
    url = inputUrl
    nameRe = url.rsplit("?name=", 1)[1]
    nameRe = nameRe.rsplit("&p=", 1)[0]
    nameRe = nameRe.replace("%20", " ")

    return nameRe

def getTrans(inputUrl):
    transDict = {}

    symbols = []
    orderdate = []
    transdate = []
    ordertype = []
    orderamount = []
    orderprice = []

    # Find the person's name
    transDict['name'] = makeName(inputUrl)
    print("Finding transactions of " + transDict['name'] + "...")

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

    # package all of the data into a nice dictionary.
    transDict['symbols'] = symbols
    transDict['orderdate'] = orderdate
    transDict['transdate'] = transdate
    transDict['ordertype'] = ordertype
    transDict['orderamount'] = orderamount
    transDict['orderprice'] = orderprice

    return transDict

def performTimeLogic(transDict):
    """
        To save system resources, we are only going to check the order status
        of transactions made in the last 5 minutes. In order to perform a
        boolean operation to check this "last 5 minutes" necessity-- makeTime()
        transforms MarketWatch's <tbody> objects into python datetime objects,
        which are then calculated upon using:

            delta = now - time

            where:
                now = datetime.datetime.now()
                and
                time = makeTime(date) for date in orderdate[]

        Because 5 minutes is a long time for multiple transactions to be made,
        it is entirely possible that the first trade viewed in our scanning is
        not at all the most recent transaction. We do not want to sell stocks
        which we do not own. To address this, we will have to reverse the list
        of times. But- again- to save system processing power- this reversing
        must take place after we have secured a listing of the past 5 minutes
        transactions.
    """
    orderdate = transDict['orderdate']
    orderQueue = [] # will hold the place of the elementIndex of order components
                    # this will later be .reverse() so that we can process orders
                    # backwards (chronologically).
    dprint(debugMode,"Original time strings:\n==========")
    times = [(makeTime(date)) for date in orderdate]

    dprint(debugMode,"\nNew time objects:\n==========")
    for time in times:
        dprint(debugMode,str(time))

    timeIndex = 0
    dprint(debugMode,"\nChecking...\n==========")
    for time in times:
        dprint(debugMode,"Checking " + str(time))
        #time zone is one hour ahead, so fix that.
        now = datetime.datetime.now() + datetime.timedelta(hours=1)

        isStillSameDay = (
        time.year == now.year and
        time.month == now.month and
        time.day == now.day )

        # go for as long as we are in the current date.
        if isStillSameDay:
            delta = now - time
            if delta < datetime.timedelta(minutes=5):
                dprint(debugMode,"Order added to queue.")
                orderQueue.append(int(timeIndex))
                # makeTicket(timeIndex,inputUrl)
            else:
                dprint(debugMode,"Not within 5 minutes.")
            timeIndex+=1
        else:
            dprint(debugMode,"\nDone finding times. Preparing orders/Exiting.\n") # for debugging
            break
    dprint(debugMode,"There are " + str(len(orderQueue)) + " order(s) to copy.\n")

    return orderQueue

def makeTime(dateString):
    txt = dateString
    dprint(debugMode,txt)

    re1='(\\d+)'	# Integer Number 1
    re2='.*?'	# Non-greedy match on filler
    re3='(\\d+)'	# Integer Number 2
    re4='.*?'	# Non-greedy match on filler
    re5='(\\d+)'	# Integer Number 3
    re6='.*?'	# Non-greedy match on filler
    re7='(\\d+)'	# Integer Number 4
    re8='.*?'	# Non-greedy match on filler
    re9='(\\d+)'	# Integer Number 5
    re10='((?:[a-z][a-z0-9_]*))'	# Variable Name 1

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
        month=int(m.group(1))
        day=int(m.group(2))
        year=int(m.group(3)) + 2000
        hour=int(m.group(4))
        minute=int(m.group(5))
        meridiem=m.group(6)

    # there will most likeley be a bug here at 12am, but the market isn't open then...
    if meridiem == 'p' and hour != 12:
        hour = int(hour)+12

    time = datetime.datetime(year, month, day, hour, minute, 0)

    return time

def makeHash(inputString):
    command = "echo -n \"" + inputString + "\" | md5 -q"
    output = subprocess.check_output(command, shell=True)

    return output

f = open('transactions.log','a') # for saving transactions

def makeTicket(transDict,elementIndex,inputUrl):

    ticketString = (
        str(transDict['name']) +
        ' --- ' +
        str(transDict['symbols'][elementIndex]) +
        ' --- ' +
        str(transDict['orderprice'][elementIndex]) +
        ' --- ' +
        str(transDict['orderamount'][elementIndex]) +
        ' --- ' +
        str(transDict['ordertype'][elementIndex]) +
        ' --- ' +
        str(transDict['orderdate'][elementIndex]) +
        ' --- ' +
        str(transDict['transdate'][elementIndex]))

    hashString = makeHash(ticketString)

    # search (grep) the transactions file to see if this order has been placed
    proc = subprocess.Popen(["cat transactions.log | grep -i " + hashString], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if out == "": # grep will return empty if it can't find a matching hash.
        print("Adding new transaction...")

        ticketEntry = ticketString + ' --- ' + str(hashString)
        f.write(ticketEntry) # write the name and ticket to the file.

        import buy
        buy.order(inputUrl,transDict['symbols'][elementIndex],transDict['orderamount'][elementIndex],transDict['ordertype'][elementIndex])

    else:
        dprint(debugMode,"Order already processed.")

def copyTrades(inputUrl):
    # get the necessary data from a user's transaction <table>
    transDict = getTrans(inputUrl)

    # make a list of trades made in the past 5 minutes (according to the <table>)
    orderQueue = performTimeLogic(transDict)

    """If there were any orders made in the past 5 minutes, check to see if they
    have already been ordered. If they haven't been ordered, order them and
    generate a receipt."""
    if len(orderQueue) == 0:
        dprint(debugMode,"No orders. Clearing.")
    else:
        orderQueue.reverse() # begin chronologically

        for orderNumber in orderQueue:
            makeTicket(transDict, orderNumber, inputUrl)




# while True:
#     print("Scanning")
#     getTrans("http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=The%20Cooler%20James%20McGregor&p=1510238")
#     # time.sleep(30)

# # James Account
for n in range(5):
    copyTrades("http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=The%20Cooler%20James%20McGregor&p=1510238")









#
