import re
import json
import moira
import time
import requests
from moira import moira
from bs4 import BeautifulSoup
import login as l


# SET UP MOIRA
token = l.login()
game = 'meisenheimer'


while True:
    #time.sleep(1)
    astring = moira.stock_search(token, game, 'TSLA')
    print astring['price']
    if float(astring['price']) >= 210:
        print 'yes, selling 100 shares'
        moira.order(token, 'meisenheimer', 'Sell', 'STOCK-XNAS-TSLA', 100)
    else:
        print 'no'
