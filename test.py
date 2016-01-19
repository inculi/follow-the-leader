# Test

import moira
import requests
from moira import moira
from googlefinance import getQuotes
from bs4 import BeautifulSoup
import json

"""
    Using BeautifulSoup, this will scrape a game's user data. Using this data,
    we can rank player performance, and find the trades that they have used.
"""

# setting up BeautifulSoup
url = "http://www.marketwatch.com/game/stock-fears/ranking"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# find user names and place them in a list
tdrank = soup.find_all("td", {"class" : "rank"})
ranks = []
tdnames = soup.find_all("td", {"class" : "name"})
names = []
tdreturns = soup.find_all("td", {"class" : "numeric positive"})
returns = []
tdurls = soup.find_all("tr")
urls = []

for item in tdrank:
    good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
    ranks.append(good_data)

for item in tdnames:
    good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
    names.append(good_data)

for item in tdreturns:
    good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
    returns.append(good_data)

for item in tdurls:
    good_data = item.text.replace("\t", "").replace("\r", "").replace("\n", "")
    urls.append(good_data)

print ranks
print names
print returns
print urls



"""
    NOTE:
    On the rankings page for a given game, the names of the users are held in
    a <td> with the class "name", and the link to their profile (with its data) is held in
    a lower <a href>.
"""
