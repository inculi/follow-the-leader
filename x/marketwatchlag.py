import moira
from moira import moira
from googlefinance import getQuotes
import json

# SET UP MOIRA
token = moira.get_token('manwholikespie@gmail.com', 'password')
game = 'hack-the-system'

stocks = moira.get_current_holdings(token, game)
prices = [stocks[x].current_price for x in stocks]
#print prices

def analyze(stockTicker):
    """
    Feed the ticker string to googlefinance's "getQuotes" function--
    allowing us to retrieve the real time price. At least I hope
    it is in real time.

    :param stockTicker: String of the stock ticker you wish to analyze
    """

    quotes = getQuotes(stockTicker)
    print json.dumps(quotes, indent=2)

    # I'll let it print out the full data for now... I want to know the time
    # and stuff, but eventually I will have it filter for just the price :)
    # then I can have that price be saved in a .CSV so that I can graph and
    # analyze later or something.

def analyzeM(stockTicker):
    """
    Feed the ticker string to moira's stock_search function--
    allowing us to retrieve the [hopefully] lagging time.

    :param stockTicker: String of the stock ticker you wish to analyze
    """
    price = moira.stock_search(token,game,stockTicker)
    print price


# Begin main function
for x in xrange(0,5):
    analyze('AAPL')
    analyzeM('AAPL')
