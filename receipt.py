import re
import os
import requests
import datetime
import subprocess
import pandas as pd
import mmutils as mm
from moira import moira
from bs4 import BeautifulSoup

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
    print("Finding transactions of " + name[0] + "...")
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

    # check dates of transactions to find ones placed in last 5 minutes
    times = []
    for date in orderdate:
        times.append(makeTime(date))

    timeIndex = 0
    for time in times:
        now = datetime.datetime.now()

        isStillSameDay = (
        time.year == now.year and
        time.month == now.month and
        time.day == now.day )

        # go for as long as we are in the current date.
        if isStillSameDay:
            delta = now - time
            # print(delta)
            # print(delta < datetime.timedelta(minutes=5))
            if delta < datetime.timedelta(minutes=5):
                print("Order added to queue.")
                makeTicket(timeIndex)

            timeIndex+=1
        else:
            break

def makeHash(inputString):
    command = "echo -n \"" + inputString + "\" | md5 -q"
    output = subprocess.check_output(command, shell=True)

    return output

def makeTime(dateString):
    txt = dateString

    re1='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# month
    re2='.*?'	# Non-greedy match on filler
    re3='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# day
    re4='.*?'	# Non-greedy match on filler
    re5='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# year
    re6='.*?'	# Non-greedy match on filler
    re7='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# hour
    re8='.*?'	# Non-greedy match on filler
    re9='((?:(?:[0-2]?\\d{1})|(?:[3][01]{1})))(?![\\d])'	# minute
    re10='(.)'	# am/pm

    rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10,re.IGNORECASE|re.DOTALL)
    m = rg.search(txt)
    if m:
        month=int(m.group(1))
        day=int(m.group(2))
        year=int(m.group(3)) + 2000
        hour=int(m.group(4))
        minute=int(m.group(5))
        meridiem=m.group(6)

    if meridiem == 'p':
        hour = int(hour)+12
    time = datetime.datetime(year, month, day, hour, minute, 0)
    return time

ticketStrings = []
f = open('transactions.log','a') # for saving transactions

def makeTicket(elementIndex):
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
            ticketEntry = str(name[0]) + " --- " + str(output)
            f.write(ticketEntry) # write the name and ticket to the file.

getTrans("http://www.marketwatch.com/game/summit-high-school-economics-club-2015-2016/portfolio/transactionhistory?name=Andrew%20Hollenbaugh&p=1215199")
