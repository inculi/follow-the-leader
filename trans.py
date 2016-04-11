# internal
import re
import os
import time
import datetime
import subprocess
import cPickle as pickle

# external
import requests
from moira import moira
from bs4 import BeautifulSoup

# self-made
import buy
import mmutils as mm
from jrtools import *

"""
Make a function that finds the difference between the two dictionaries, and
    returns those stocks that have changed and the amount to which they have
    changed.

If there has been a change in the holdings, make the necessary changes to our
    own holdings, and update the pickle file to respect the report of his
    latest holdings.

Else if the dictionaries are the same, leave the pickle file and start scanning
    another user (or just sleep and prepare to scan again in a little while).
"""

debugMode = True # set to true to see current actions

def makeName(inputUrl):
    nameRe = inputUrl.rsplit("?name=", 1)[1]
    nameRe = nameRe.rsplit("&p=", 1)[0]
    nameRe = nameRe.replace("%20", " ").replace("%3F","?")

    return nameRe

def makeGameName(inputUrl):
    nameRe = inputUrl.rsplit(".com/game/", 1)[1]
    nameRe = nameRe.rsplit("/portfolio/", 1)[0]
    # thought: I think I'm going to leave the dashes in the name, for the sake
    # of being able to manipulate holdings.log with better ease...

    return nameRe

def makePlayerId(inputUrl):
    nameRe = inputUrl.rsplit("&p=", 1)[1]
    return nameRe

def copyTrades(inputUrl):
    """Create a dictionary of a user's current holdings.
    Example output:
    {'NKE Short': 581, 'SONC Buy': 943}
    """
    # set up soup of beauty
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content,"html.parser")

    holdings = {} # initialize a dictionary to store current holdings

    holdingTag = soup.select("tr[data-insttype=Stock]") # find the stock <tr>(s)
    for item in holdingTag:
        stockName = str(item.attrs['data-ticker'] + " " + item.attrs['data-type'])
        holdings[stockName] = int(float(item.attrs['data-shares']))

    return holdings

def findTradeDifference(inputUrl):
    # grab current holdings
    currentHoldings = copyTrades(inputUrl)

    # look for holdings according to our last scan
    pickleFileName = makePlayerId(inputUrl) + " " + makeGameName(inputUrl) + ".log"
    try: oldHoldings = pickle.load( open( pickleFileName, "rb" ) ) # load holdings dictionary
    except IOError:
        dprint(debugMode,"File did not exist. Creating it now.")
        os.system("touch " + pickleFileName.replace(" ","\\ "))
        oldHoldings = oldHoldings = {}
    except EOFError:
        dprint(debugMode,"File was empty. Making an empty 'oldHoldings'.")
        oldHoldings = {} # just make it empty

    # find the difference between the two 'holdings' dictionaries
    if oldHoldings == currentHoldings:
        dprint(debugMode,"They are the same.")
        return 0 # they are the same. don't worry about saving/buying anything.
    else:
        # initialize a dictionary to store the changes to our holdings.
        deltaHoldings = {}

        # the stocks where we either sold all of or purchased for the first time
        bought = [stock for stock in currentHoldings if stock not in oldHoldings]
        sold = [stock for stock in oldHoldings if stock not in currentHoldings]
        for item in bought:
            deltaHoldings[item] = currentHoldings[item]
        for item in sold:
            deltaHoldings[item] = -1 * (oldHoldings[item])

        # check to see if we bought/sold any more of a stock we owned
        currentCacheDict = dict(currentHoldings)
        oldCacheDict = dict(oldHoldings)
        for item in bought:
            del currentCacheDict[item]
        for item in sold:
            del oldCacheDict[item]

        if currentCacheDict == oldCacheDict:
            # other than the stocks we bought for the first time (or sold all of),
            # nothing else was changed.
            dprint(debugMode,"No previously-owned stocks were altered.")

            pickle.dump( currentHoldings, open( pickleFileName, "wb" ) ) # save
            return deltaHoldings
        else:
            # go through each dictionary, and compare the value of each of their holdings
            for holding in currentCacheDict:
                if currentCacheDict[holding] - oldCacheDict[holding] == 0:
                    pass # means the stock wasn't changed
                else:
                    deltaHoldings[holding] = currentCacheDict[holding] - oldCacheDict[holding]

            pickle.dump( currentHoldings, open( pickleFileName, "wb" ) ) # save
            return deltaHoldings

def buyTrades(deltaHoldings,inputUrl):
    for item in deltaHoldings:
        ticker = item.rsplit(" ",1)[0]
        position = item.rsplit(" ",1)[1]

        if deltaHoldings[item] < 0: # means we sold something
            # deltaHoldings will be negative if we sold something
            # change the orderType to its opposite so we sell instead of Buy.
            ordType = oppositeOrd(position)
            amount = abs(deltaHoldings[item])
            print(str(ordType) + " " + str(amount) + " " + str(ticker))
            buy.order(inputUrl,ticker,amount,ordType)
        else:
            # deltaHoldings will otherwise be positive, so buy normally.
            amount = deltaHoldings[item]
            print(str(position) + " " + str(amount) + " " + str(ticker))
            buy.order(inputUrl,ticker,amount,position)

def oppositeOrd(orderType):
    if orderType.lower() == 'buy':
        return 'Sell'
    elif orderType.lower() == 'short':
        return 'Cover'
    elif orderType.lower() == 'sell':
        return 'Buy'
    elif orderType.lower() == 'cover':
        return 'Short'
    else:
        print("I don't know the opposite of this order.")
        return 1

url = "http://www.marketwatch.com/game/invest-until-you-die/portfolio/holdings?name=Colin%20Rhoades&p=1045616"
while True:
    # print(datetime.datetime.now())
    deltaHoldings = findTradeDifference(url)
    if deltaHoldings != 0:
        buyTrades(deltaHoldings,url)
