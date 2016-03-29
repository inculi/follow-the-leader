#from googlefinance import getQuotes
from bs4 import BeautifulSoup
from moira import moira
import re
import requests
import pickle

# set up moira
username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'moiratestone'
token = moira.get_token(username, password)

def makeName(inputUrl):
    url = inputUrl
    nameRe = url.rsplit("?name=", 1)[1]
    nameRe = nameRe.rsplit("&p=", 1)[0]
    nameRe = nameRe.replace("%20", " ")

    return nameRe

def searchStock(tickerSymbol,option):
    searchData = str(moira.stock_search(token, game, tickerSymbol))
    if option == 'name':
        re1='.*?'	# Non-greedy match on filler
        re2='\\\'.*?\\\''	# Uninteresting: strng
        re3='.*?'	# Non-greedy match on filler
        re4='\\\'.*?\\\''	# Uninteresting: strng
        re5='.*?'	# Non-greedy match on filler
        re6='(\\\'.*?\\\')'	# Single Quote String 1

        rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
        m = rg.search(searchData)
        if m:
            strng1=m.group(1)
        return (strng1).replace("'","")

    if option == 'price':
        re1='.*?'	# Non-greedy match on filler
        re2='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 1

        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(searchData)
        if m:
            float1=m.group(1)
        return float1

def buyStock(token, game, action, tickerSymbol, amt, times):
    print("Buying...")
    for x in xrange(0,times):
        print("moira.order(token, game, " + str(action) + ", " + str(tickerSymbol) + ", " + str(amt) + ")")
        orderStatus = moira.order(token, game, str(action), str(tickerSymbol), str(amt))
        if orderStatus[0] == True:
            print("Order successful.")
            break
        else:
            # Volume restriction bypass
            print("\nOrder Failed. Fixing now...")
            # find the legal transaction limit
            newAmount = int((str(orderStatus[1]).rsplit("volume restriction ", 1)[1]).rsplit(".", 1)[0])

            times = amt/newAmount # the amount of legal transactions we can make
            remainder =  amt - (newAmount * (amt/newAmount)) # excess amount

            # break up the large order into smaller, legal transactions
            for x in range(times):
                moira.order(token, game, action, tickerSymbol, newAmount)

            # order the excess amount
            moira.order(token, game, action, tickerSymbol, remainder)

    print("Transaction complete.")

def getNetWorth():
    money = moira.get_portfolio_data(token,game)
    # print money
    return float(money['net_worth'])

def getOthersHoldingsAmount(inputUrl,inputTicker,orderType):
    # make it direct to holdings instead of transactions.
    holdingsUrl = inputUrl.replace("/transactionhistory?","/holdings?")

    # Soup of Beauty setup.
    r = requests.get(holdingsUrl)
    soup = BeautifulSoup(r.content, "html.parser")
    rowTag = soup.select("tr[data-ticker=" + inputTicker + "] td.equity p.secondaryfield")
    for item in rowTag:
        holdingAmount = item.text.replace("\n","").replace("\t","").replace("\r","").replace(",","")
        if ('Buy' in holdingAmount) and (orderType == 'Buy'):
            holdingAmount = int(holdingAmount.rsplit(" / ", 1)[0])
            return holdingAmount
        elif ('Short' in holdingAmount) and (orderType == 'Short'):
            holdingAmount = int(holdingAmount.rsplit(" / ", 1)[0])
            return holdingAmount
        else:
            name = makeName(inputUrl=)
            print(name + " does not own " + inputTicker + " in '" + orderType + "' form.")
            return 0

def addHolding(inputTicker,orderType,amount):
    holdings = pickle.load( open( "holdings.log", "r" ) ) # load holdings dictionary
    keyString = inputTicker + ' ' + orderType # ex: holdings['AAPL Buy']

    if keyString in holdings:
        # if an entry exists for AAPL already, just add the new shares to the current amount
        holdings[keyString] += amount
    else:
        # if an entry does not exist for AAPL, create a new one with the current amount.
        holdings = { keyString : amount }

    pickle.dump( holdings, open( "holdings.log", "w" ) ) # save

def getHoldings(inputTicker,orderType):
    holdings = pickle.load( open( "holdings.log", "r" ) ) # load holdings dictionary
    keyString = inputTicker + ' ' + orderType # ex: holdings['AAPL Buy']

    if keyString in holdings:
        # if an entry exists for AAPL already, just add the new shares to the current amount
        return holdings[keyString]
    else:
        print("I do not own any '" + inputTicker + "' in '" + orderType + "'.")
        return 0

def order(inputUrl,inputTicker,amount,ordType):
    url = inputUrl
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # get our two networths
    networth_tag = soup.select("li span")
    networth = float(networth_tag[1].text.replace("$","").replace(",",""))
    myNetWorth = getNetWorth()

    symbol = searchStock(inputTicker,'name')
    price = searchStock(inputTicker,'price')

    if price < 2.00:
        print("I cannot buy that stock, as it is under $2.")
        return 1

    # amoutToSpend = (price * ((myNetWorth/networth) * amount))
    if (ordType.lower() == 'buy') or (ordType.lower() == 'short'):
        amount = int(round((myNetWorth/networth) * amount)) # change the amount to reflect our $
    else:
        # find the amount of inputTicker a given user owns.
        if orderType.lower() == 'sell':
             # to sell, we have to use the amount we bought.
            currentHoldingsAmount = getOthersHoldingsAmount(inputUrl,inputTicker,'Buy')
            myCurrentHoldingsAmount = getHoldings(inputTicker,'Buy')
        elif orderType.lower() == 'cover':
             # to cover, we have to use the amount we shorted.
            currentHoldingsAmount = getOthersHoldingsAmount(inputUrl,inputTicker,'Short')
            myCurrentHoldingsAmount = getHoldings(inputTicker,'Short')

        amount = int( round( (amount / currentHoldingsAmount) * myCurrentHoldingsAmount) )

    # amount of times the for loop will run. Eventually this will have to be changed,
    # as the volume restrictions prevent most orders from going through.
    times = 1

    buyStock(token, game, ordType, symbol, amount, times)
    addHolding(inputTicker,orderType,amount)
