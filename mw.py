from moira import moira
import time
from googlefinance import getQuotes
import json
import login as l

# SET UP MOIRA
token = l.login()
game = 'meisenheimer'


for x in xrange(0,20):
    time.sleep(5)
    astring = moira.stock_search(token, game, 'FLDM')
    print astring
