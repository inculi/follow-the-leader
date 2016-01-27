import re
import json
import time
import moira
import random
import requests
import numpy as np
import pandas as pd
from moira import moira
from bs4 import BeautifulSoup
#from googlefinance import getQuotes


"""
    Using BeautifulSoup, this will scrape a game's user data. Using this data,
    we can rank player performance, and find the trades that they have used.
"""

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
    for x in xrange (0,int(round(((1.0/3.0)*total))),10):
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

# constants that we will need later on in the program.
ranks = []
names = []
returns = []
player_urls = []
transaction_urls = []
performance_urls = []
networths = []
total_cash_returns = []
todays_percent_returns = []
amtOfTrades = []

def pageScan(pageurl):
    # url = "http://www.marketwatch.com/game/bijans/ranking"
    # setting up BeautifulSoup
    url = pageurl
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # find ranks, names, returns and urls and place them in lists.
    td_rank = soup.find_all("td", {"class" : "rank"})

    td_names = soup.find_all("td", {"class" : "name"})

    player_url = soup.findAll('a', href=re.compile('/portfolio/holdings\?name='))

    td_networth = soup.find_all("em")

    # total cash returns
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        cash_return_column = row.findAll('td')[4:5]
        for item in cash_return_column:
            if 'B' not in item.text:
                total_cash_returns.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$", "").replace(",","")))
            if 'B' in item.text:
                total_cash_returns.append(float(0))

    # today's percent returns
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        percent_return_column = row.findAll('td')[3:4]
        for item in percent_return_column:
            if 'B' not in item.text:
                todays_percent_returns.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("%", "").replace(",","")))
            if 'B' in item.text:
                todays_percent_returns.append(float(0))

    # Filter for data
    for item in td_rank:
        ranks.append(item.text.replace("\t", "").replace("\r", "").replace("\n", ""))

    for item in td_names:
        names.append(item.text.replace("\t", "").replace("\r", "").replace("\n", ""))

    for item in td_networth:
        networths.append(float(item.text.replace("$","").replace(",","").replace(")","").replace("(","-")))

    for item in player_url:
        url = 'http://marketwatch.com' + str(item.get('href'))
        player_urls.append(url)
        transaction_urls.append(url.replace("holdings", "transactionhistory"))
        performance_urls.append(url.replace("holdings", "performance"))

    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        trades_column = row.findAll('td')[5:6]
        for item in trades_column:
            amtOfTrades.append(float(item.text))

def gameScan(gameName):
    pageUrls = pageCounter(gameName)
    index = 0
    for url in pageUrls:
        index+=1
        pageScan(url)
        # time.sleep(1)
        print("Finished " + str(index) + " of " + str(len(pageUrls)))



games = [] # list that the game names will be stored in (for processing by gameScan)

def getGames(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    index = url.find('sort=')
    for item in soup.find_all("td", {'class' : 'name'}):
        #print item
        out = str(item).rsplit("href=\"/game/", 1)[1]
        games.append(out.rsplit("\" title", 1)[0])

def getGameURLs(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    index = url.find('sort=')

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
            for page in xrange (0, 100, 10):
                getGames(url[:index] + 'index=' + str(page) + '&' + url[index:])

    for item in games:
        print item


### MAIN FUNCTION
getGameURLs("http://www.marketwatch.com/game/find?sort=NumberOfPlayers&descending=True")

gameCountIndex = 0
for game in games:
    gameCountIndex += 1
    print("Scanning " + str(game) + ": (" + str(gameCountIndex) + "/" + str(len(games)) + ")")
    gameScan(game)
del gameCountIndex

# print our findings
print("\n\nRanks:")
print(len(ranks))
print("\n\nNames:")
print(len(names))
print("\n\nCash Returns:")
print(len(total_cash_returns))
print("\n\nPercent Returns:")
print(len(todays_percent_returns))
print("\n\nPlayer URLs:")
print(len(player_urls))
print("\n\Performance URLs:")
print(len(performance_urls))

d = {
    'Name' : pd.Series(names, index=ranks),
    'Net Worth' : pd.Series(networths, index=ranks),
    'Today\'s Returns' : pd.Series(todays_percent_returns, index=ranks),
    'Total Cash Returns' : pd.Series(total_cash_returns, index=ranks),
    'Trades' : pd.Series(amtOfTrades, index=ranks),
    'Player URL' : pd.Series(player_urls, index=ranks),
    'Transaction URL' : pd.Series(transaction_urls, index=ranks),
    'Performance URL' : pd.Series(performance_urls, index=ranks)
    }

df = pd.DataFrame(d)
print df
df.to_csv("dataframe2.csv")









































#
