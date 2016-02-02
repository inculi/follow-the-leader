import re
import requests
from bs4 import BeautifulSoup

def playTime(performanceURL):
    url = performanceURL
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    days_data = soup.find_all("p")
    for item in days_data:
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
                days_played = int(int1)
                return days_played
