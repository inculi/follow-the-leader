import re
import requests
from bs4 import BeautifulSoup

temp = {'game' : [], 'date' : []}
games = {'game' : [], 'date' : []}

def getGames(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    index = url.find('sort=')
    for item in soup.find_all("td", {'class' : 'name'}):
        out = (str(item).rsplit("href=\"/game/", 1)[1]).rsplit("\" title", 1)[0]
        temp['game'].append(out)

    for item in soup.find_all("td", {'class' : 'enddate'}):
        out = (str(item).rsplit("enddate\">", 1)[1]).rsplit("</td>", 1)[0]
        temp['date'].append(out)

def removeOld():
    for x in range(0, len(temp['game'])):
        if "days" in temp['date'][x]:
            if int(temp['date'][x].rsplit(" days", 1)[0]) > 7:
                print int(temp['date'][x].rsplit(" days", 1)[0])
                games['game'].append(temp['game'][x])
                games['date'].append(temp['date'][x])

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

getGameURLs("http://www.marketwatch.com/game/find?sort=NumberOfPlayers&descending=True")
removeOld()

for item in games['game']:
    print item
for item in games['date']:
    print item
