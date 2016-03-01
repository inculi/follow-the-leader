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

debugMode = True

#Output
symbols = []
orderdate = []
transdate = []
ordertype = []
orderamount = []
orderprice = []
name = []

def getTrans(inputUrl):
    # Find the person's name
    url = inputUrl
    nameRe = url.rsplit("?name=", 1)[1]
    nameRe = nameRe.rsplit("&p=", 1)[0]
    nameRe = nameRe.replace("%20", " ")
    name.append(nameRe)
    # print("Finding transactions of " + name[0] + "...")
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

    # So that I can place the individual's name next to their transaction (so
    # that transactions.log is better organized)
    # mm.populate(names,name,len(symbols))

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #                      DEBUGGING - show the data we have
    # mm.printAll(symbols)
    # mm.printAll(orderdate)
    # mm.printAll(transdate)
    # mm.printAll(ordertype)
    # mm.printAll(orderamount)
    # mm.printAll(orderprice)
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # old way of doing it //IGNORE
    # times = []
    # for date in orderdate:
    #     times.append(makeTime(date))
    #     print("There are now " + str(len(times)) + " in times[]")

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
    if len(orderQueue) == 0:
        dprint(debugMode,"clearing")
        clearGlobalLists()
    else:
        # print(orderQueue)
        orderQueue.reverse() # begin chronologically
        # print(orderQueue)

        # old way of doing it...
        # for x in xrange(0,len(orderQueue)):
        #     makeTicket(orderQueue[x],inputUrl)


        for orderNumber in orderQueue:
            makeTicket(orderNumber, inputUrl)
        clearGlobalLists()

def makeHash(inputString):
    command = "echo -n \"" + inputString + "\" | md5 -q"
    output = subprocess.check_output(command, shell=True)

    return output

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

    if meridiem == 'p' and hour != 12:
        hour = int(hour)+12

    time = datetime.datetime(year, month, day, hour, minute, 0)

    return time

f = open('transactions.log','a') # for saving transactions

def makeTicket(elementIndex,inputUrl):
    ticketStrings = []
    # make it go for however many tickers we have
    # for x in xrange(0,len(symbols)):
    ticketString = str(symbols[elementIndex]) + ';' + str(orderdate[elementIndex]) + ';' + str(transdate[elementIndex]) + ';' + str(ordertype[elementIndex]) + ';' + str(orderamount[elementIndex]) + ';' + str(orderprice[elementIndex])
    ticketStrings.append(ticketString)

    for ticket in ticketStrings:
        hashString = makeHash(ticket)

        # search (grep) the transactions file to see if this order has been placed
        proc = subprocess.Popen(["cat transactions.log | grep -i " + hashString], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if out == "": # grep will return empty if it can't find a matching hash.
            print("Adding new transaction...")
            ticketEntry = str(name[0]) + " --- " + str(hashString)
            f.write(ticketEntry) # write the name and ticket to the file.

            # I am fairly certain that it should work as is, but just in case...
            # if ordertype[elementIndex] == 'Buy':
            #     oType = 'Buy'
            # if ordertype[elementIndex] == 'Sell':
            #     oType = 'Sell'
            # if ordertype[elementIndex] == 'Short':
            #     oType = 'Short'
            # if ordertype[elementIndex] == 'Cover':
            #     oType = 'Cover'
            import buy
            buy.order(inputUrl,symbols[elementIndex],orderamount[elementIndex],ordertype[elementIndex])
        else:
            dprint(debugMode,"Order already processed.")

def clearGlobalLists():
    # clear global lists for next iteration (assuming there is a
    # " while True: getTrans() " looping at the end of this file)
    symbols[:] = []
    orderdate[:] = []
    transdate[:] = []
    ordertype[:] = []
    orderamount[:] = []
    orderprice[:] = []
    name[:] = []

# while True:
#     print("Scanning")
#     getTrans("http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=The%20Cooler%20James%20McGregor&p=1510238")
#     # time.sleep(30)


# Good ol' Andrew boy
# getTrans("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")


# # James Account
getTrans("http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=The%20Cooler%20James%20McGregor&p=1510238")









#
