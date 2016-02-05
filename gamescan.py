import re
import json
import time
import moira
import random
import requests
import playtime as play # the function I wrote to find the days played of a player
import numpy as np
import pandas as pd
import games as game
# import userscan as user
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
numDaysPlayed = []

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
        performanceString = url.replace("holdings", "performance")
        performance_urls.append(performanceString)
        numDaysPlayed.append(play.playTime(performanceString))

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

### MAIN FUNCTION
print("Finding games...")
game.getGameURLs("http://www.marketwatch.com/game/find?sort=NumberOfPlayers&descending=True")
games = game.removeOld()
games = set(games) # remove duplicates
print("Found " + str(len(games)) + " games.")

# begin scanning games and their users
gameCountIndex = 0
for game in games:
    gameCountIndex += 1
    print("Scanning " + str(game) + ": (" + str(gameCountIndex) + "/" + str(len(games)) + ")")
    gameScan(game)
del gameCountIndex

# print our findings
print("\nRanks:")
print(len(ranks))
print("\nNames:")
print(len(names))
print("\nCash Returns:")
print(len(total_cash_returns))
print("\nPercent Returns:")
print(len(todays_percent_returns))
print("\nPlayer URLs:")
print(len(player_urls))
print("\nPerformance URLs:")
print(len(performance_urls))

# transform lists into Series
ranks_series = pd.Series(ranks, index=ranks)
names_series = pd.Series(names, index=ranks)
networths_series = pd.Series(networths, index=ranks)
todays_percent_returns_series = pd.Series(todays_percent_returns, index=ranks)
total_cash_returns_series = pd.Series(total_cash_returns, index=ranks)
amtOfTrades_series = pd.Series(amtOfTrades, index=ranks)
player_urls_series = pd.Series(player_urls, index=ranks)
transaction_urls_series = pd.Series(transaction_urls, index=ranks)
performance_urls_series = pd.Series(performance_urls, index=ranks)
numDaysPlayed_series = pd.Series(numDaysPlayed, index=ranks)

d = {
    'Rank' : ranks_series,
    'Name' : names_series,
    'Net Worth' : networths_series,
    'Today\'s Returns' : todays_percent_returns_series,
    'Total Cash Returns' : total_cash_returns_series,
    'Trades' : amtOfTrades_series,
    'Player URL' : player_urls_series,
    'Transaction URL' : transaction_urls_series,
    'Performance URL' : performance_urls_series,
    'Days Played' : numDaysPlayed_series,
    }

df = pd.DataFrame(d)

# Filter out those with negative returns and with barely any data
df = df[df['Total Cash Returns'] > 0]
df = df[df['Days Played'] > 0]
df = df[df['Trades'] > 1]

print df
df.to_csv("unsorted.csv")

### Perform some calculations on the remaining users
df['total percent returns'] = (df['Total Cash Returns'] / (df['Net Worth'] - df['Total Cash Returns']) * 100)
df = df.sort_values(by='total percent returns', ascending=False)
# only take the top 1000 users
df = df[:1000]
df.to_csv("top 1000.csv")

# -----
df['total percent returns per day'] = df['total percent returns'] / df['Days Played']
df = df.sort_values(by='total percent returns per day', ascending=False)
df = df[:500]
df.to_csv("top 500.csv")

# -----
df['trades per day'] = df['Trades'] / df['Days Played']
df['percent returns per trade'] = df['total percent returns'] / df['Trades']
df = df.sort_values(by='trades per day', ascending=False)
df = df[:250]
df.to_csv("top 250.csv")
#
