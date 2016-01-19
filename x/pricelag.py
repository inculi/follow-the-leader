from googlefinance import getQuotes
import moira
import json

# set up moira


def analyze(stockTicker):
    """
    Feed the ticker string to googlefinance's "getQuotes" function-
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

# set up moira





# Begin main function
for x in xrange(0,5):
    analyze('AAPL')
