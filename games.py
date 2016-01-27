import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup

games = []

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

getGameURLs("http://www.marketwatch.com/game/find?sort=NumberOfPlayers&descending=True")
