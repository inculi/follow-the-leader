#from googlefinance import getQuotes
from bs4 import BeautifulSoup
from moira import moira
import re

# set up moira
username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'meisenheimer'
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
        # moira.order(token, game, action, tickerSymbol, amt)
        print("moira.order(" + str(token) + str(game) + str(action) + str(tickerSymbol) + str(amt) + ")")
    print("Transaction complete.")

def getNetWorth():
    money = moira.get_portfolio_data(token,game)
    return float(money['net_worth'])

def order(inputUrl,inputTicker,amount,ordType):
    url = inputUrl
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    networth_tag = soup.select("li span")
    networth = float(networth_tag[1].text.replace("$","").replace(",",""))

    myNetWorth = getNetWorth()

    symbol = searchStock(inputTicker,'name')
    price = searchStock(inputTicker,'price')

    # amoutToSpend = (price * ((myNetWorth/networth) * amount))
    amount = ((myNetWorth/networth) * amount) # change the amount to reflect our $

    # amount of times the for loop will run. Eventually this will have to be changed,
    # as the volume restrictions prevent most orders from going through.
    times = 1

    buyStock(token, game, ordType, symbol, amount, times)
