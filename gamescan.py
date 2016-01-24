import re
import json
import time
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup
from googlefinance import getQuotes


"""
    Using BeautifulSoup, this will scrape a game's user data. Using this data,
    we can rank player performance, and find the trades that they have used.
"""

# constants that we will need later on in the program.
ranks = []
names = []
returns = []
player_urls = []
transaction_urls = []

def pageCounter(gameName):
    """
        Find the URLs of all the pages of a game. MarketWatch only allows you to
        view the information of 10 players at a time. This fixes that problem.

    :output:            Returns a list of page URLs.

    :param gameName:    The name of the game you wish to scan. It can be found
                        in the URL of the game's main page. Ex: stock-game-2016
    """
    pages = [] # list to hold all the 10-user long pages of a game

    # setting up BeautifulSoup
    url = "http://www.marketwatch.com/game/" + gameName + "/ranking"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # define constants
    total = 0 # int that represents the amount of players in the game

    # A <p> of at the bottom of the page contain the amount of players (1-10 of)
    people = soup.find_all("p")
    for item in people:
        if item.parent.name == 'nav':
            re1='.*?'	# Non-greedy match on filler
            re2='\\d+'	# Uninteresting: int
            re3='.*?'	# Non-greedy match on filler
            re4='\\d+'	# Uninteresting: int
            re5='.*?'	# Non-greedy match on filler
            re6='(\\d+)'	# Integer Number 1

            rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
            m = rg.search(item.text)
            if m:
                int1=m.group(1)
                total = int(int1)
                print("There are " + str(total) + " players in the game.")

    # find the URLs of all the pages of a game
    for x in xrange (0,total,10):
        # http://www.marketwatch.com/game/stock-fears/ranking?index=10&total=974
        if x < 10: # the first page's url can do with or without the index pieces
            url = ("http://www.marketwatch.com/game/" +
            gameName +
            "/ranking"
            )
        else:
            url = (
            "http://www.marketwatch.com/game/" +
            gameName +
            "/ranking?index=" +
            str(x) +
            "&total=" +
            str(total)
            )
        pages.append(url)

    return pages

def pageScan(pageurl):
    # url = "http://www.marketwatch.com/game/stock-fears/ranking"
    # setting up BeautifulSoup
    url = pageurl
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # find ranks, names, returns and urls and place them in lists.
    td_rank = soup.find_all("td", {"class" : "rank"})

    td_names = soup.find_all("td", {"class" : "name"})

    td_returns = soup.find_all("td", {"class" : "numeric positive"})

    player_url = soup.findAll('a', href=re.compile('/portfolio/holdings\?name='))


    # Filter for data
    for item in player_url:
        #print(item.get('href'))
        url = 'http://marketwatch.com' + str(item.get('href'))
        player_urls.append(url)

    for item in td_rank:
        good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
        #print(good_data)
        ranks.append(good_data)

    for item in td_names:
        good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
        #print(good_data)
        names.append(good_data)

    for item in td_returns:
        good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
        #print(good_data)
        returns.append(good_data)

    # Transactions
    for item in player_urls:
        # Transform the url array to make those urls "transaction" instead of "holdings"
        # print item.replace("holdings", "transactionhistory")
        transaction_urls.append(item.replace("holdings", "transactionhistory"))

def gameScan(gameName):
    pageUrls = pageCounter(gameName)

    for url in pageUrls:
        pageScan(url)
        time.sleep(1)
        print("Finished " + str(url))

### MAIN FUNCTION ###
# gameScan("http://www.marketwatch.com/game/stock-fears/ranking")
# gameScan("http://www.marketwatch.com/game/stock-fears/ranking?index=10&total=950")

gameScan("atiseconomics2015")

# print our findings
print("\n\n")
print(ranks)
print("\n\n")
print(names)
print("\n\n")
print(returns)
print("\n\n")
print(player_urls)
print("\n\n")
print(transaction_urls)
print("\n\n")
