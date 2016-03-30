#from googlefinance import getQuotes
from bs4 import BeautifulSoup
from moira import moira
import re
import requests
import cPickle as pickle

# set up moira
username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'moiratestone'
token = moira.get_token(username, password)

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
            name = makeName(inputUrl)
            print(name + " does not own " + inputTicker + " in '" + orderType + "' form.")
            return 0

def addHolding(inputUrl,inputTicker,orderType,amount):
    """I cannot include a user's name in their dictionary key, as if they change
    their name... their holdings will no longer be monitored according to their
    name. Therefore, I must use their playerid, as I am fairly certain that
    MW keeps that the same (please oh God I hope they do).

    Just so that everything doesn't go crazy, however, I will store their name
    under their holdings{} dict just in case.
    """
    try: holdings = pickle.load( open( "holdings.log", "rb" ) ) # load holdings dictionary
    except EOFError: holdings = {} # or whatever you want

    playerName = makeName(inputUrl).replace(" ","-")
    playerId = makePlayerId(inputUrl)
    playerGame = makeGameName(inputUrl)

    # User's dictionary key. Ex: holdings['895646 stock-fears']
    playerKey = playerId + ' ' + playerGame
    keyString = inputTicker + ' ' + orderType # ex: holdings['AAPL Buy']

    if playerKey not in holdings:
        holdings[playerKey] = {} # create a dictionary for the user
        holdings[playerKey]['name'] = playerName # give the player a name

    if keyString in holdings[playerKey]:
        # if an entry exists for AAPL already, just add the new shares to the current amount
        holdings[playerKey][keyString] += amount
    else:
        # if an entry does not exist for AAPL, create a new one with the current amount.
        holdings[playerKey][keyString] = amount

    pickle.dump( holdings, open( "holdings.log", "wb" ) ) # save

def getHoldings(inputUrl,inputTicker,orderType):
    try: holdings = pickle.load( open( "holdings.log", "rb" ) ) # load holdings dictionary
    except EOFError: holdings = {} # or whatever you want

    playerName = makeName(inputUrl).replace(" ","-")
    playerId = makePlayerId(inputUrl)
    playerGame = makeGameName(inputUrl)

    # User's dictionary key. Ex: holdings['895646 stock-fears']
    playerKey = playerId + ' ' + playerGame
    keyString = inputTicker + ' ' + orderType # ex: holdings['AAPL Buy']

    if playerKey not in holdings:
        print("I do not own anything by '" + playerKey + "', aka " + playerName)
        return None

    keyString = inputTicker + ' ' + orderType # ex: holdings['AAPL Buy']

    if keyString in holdings[playerKey]:
        # if an entry exists for AAPL already, just add the new shares to the current amount
        return holdings[playerKey][keyString]
    else:
        print("I do not own any '" + inputTicker + "' in '" + orderType +
        "' bought by '" + playerKey + "', aka " + playerName)
        return None

def readAllHoldings():
    try: holdings = pickle.load( open( "holdings.log", "rb" ) ) # load holdings dictionary
    except EOFError: holdings = {}

    return holdings

def sellPlayerHoldings(inputUrl):
    try: holdings = pickle.load( open( "holdings.log", "rb" ) ) # load holdings dictionary
    except EOFError: holdings = {} # or whatever you want

    playerName = makeName(inputUrl).replace(" ","-")
    playerId = makePlayerId(inputUrl)
    playerGame = makeGameName(inputUrl)

    # User's dictionary key. Ex: holdings['895646 stock-fears']
    playerKey = playerId + ' ' + playerGame

    if playerKey not in holdings:
        print("I do not own anything by '" + playerKey + "', aka " + playerName)
        return 1

    del holdings[playerKey]['name'] # to make incrementing easier

    for x in holdings[playerKey]:
        print("Selling all of " + x)
        for y in holdings[playerKey][x]:
            yElements = y.split(" ")
            ticker = yElements[0]
            orderType = yElements[1]
            amount = holdings[playerKey][x][y]
            if amount == 0:
                pass
            else:
                if orderType.lower() == 'buy':
                    buyStock(token, game, 'Sell', ticker, amount, 1)

                elif orderType.lower() == 'short':
                    buyStock(token, game, 'Cover', ticker, amount, 1)

def order(inputUrl,inputTicker,amount,ordType):
    print('ordType: ', ordType)
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
        if ordType.lower() == 'sell':
            # to sell, we have to use the amount we bought.
            myCurrentHoldingsAmount = getHoldings(inputUrl,inputTicker,'Buy')
            if myCurrentHoldingsAmount == None:
                return 1 # I have nothing to sell

            currentHoldingsAmount = getOthersHoldingsAmount(inputUrl,inputTicker,'Buy')
            if currentHoldingsAmount == None:
                # if he sold all of his shares, he will have none left.
                # if he has none left, getOthersHoldingsAmount() will return: None
                # I cannot divide a float by a noneType, therefore I must make
                # the final fraction equivalent to 1 so I can sell 100% of my owned amt.
                currentHoldingsAmount = amount

        elif ordType.lower() == 'cover':
            # to cover, we have to use the amount we shorted.
            myCurrentHoldingsAmount = getHoldings(inputUrl,inputTicker,'Short')
            if myCurrentHoldingsAmount == None:
                return 1 # I have nothing to sell

            currentHoldingsAmount = getOthersHoldingsAmount(inputUrl,inputTicker,'Short')
            if currentHoldingsAmount == None:
                # if he sold all of his shares, he will have none left.
                # if he has none left, getOthersHoldingsAmount() will return: None
                # I cannot divide a float by a noneType, therefore I must make
                # the final fraction equivalent to 1 so I can sell 100% of my owned amt.
                currentHoldingsAmount = amount

        amount = int( round( (amount / currentHoldingsAmount) * myCurrentHoldingsAmount) )

    # amount of times the for loop will run. Eventually this will have to be changed,
    # as the volume restrictions prevent most orders from going through.
    times = 1

    buyStock(token, game, ordType, symbol, amount, times)
    if (ordType.lower() == 'sell'):
        negativeAmount = -1 * amount
        addHolding(inputUrl,inputTicker,'Buy',negativeAmount)
    elif (ordType.lower() == 'cover'):
        negativeAmount = -1 * amount
        addHolding(inputUrl,inputTicker,'Short',negativeAmount)
    else:
        addHolding(inputUrl,inputTicker,ordType,amount)
