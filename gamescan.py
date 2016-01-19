import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup
from googlefinance import getQuotes


"""
    Using BeautifulSoup, this will scrape a game's user data. Using this data,
    we can rank player performance, and find the trades that they have used.
"""

def gameScan(pageurl):
    # "http://www.marketwatch.com/game/stock-fears/ranking"
    # setting up BeautifulSoup
    url = pageurl
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find the amount of pages, and people that are in the game
    people = soup.find_all("li", {"class" : "end"})

    # re.search('(?<=-)\w+', 'spam-egg')
    for item in people:
        print item

    # find ranks, names, returns and urls and place them in lists.
    td_rank = soup.find_all("td", {"class" : "rank"})
    ranks = []
    td_names = soup.find_all("td", {"class" : "name"})
    names = []
    td_returns = soup.find_all("td", {"class" : "numeric positive"})
    returns = []
    player_url = soup.findAll('a', href=re.compile('/portfolio/holdings\?name='))
    player_urls = []
    transaction_urls = []

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

    print ranks
    print names
    print returns
    print player_urls
    print transaction_urls

### MAIN FUNCTION ###
gameScan("http://www.marketwatch.com/game/stock-fears/ranking")
