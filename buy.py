#from googlefinance import getQuotes
from bs4 import BeautifulSoup
from moira import moira
import re
import requests

# set up moira
username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'moiratestone'
token = moira.get_token(username, password)

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

    # amoutToSpend = (price * ((myNetWorth/networth) * amount))
    amount = int(round((myNetWorth/networth) * amount)) # change the amount to reflect our $

    # amount of times the for loop will run. Eventually this will have to be changed,
    # as the volume restrictions prevent most orders from going through.
    times = 1

    buyStock(token, game, ordType, symbol, amount, times)
