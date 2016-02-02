from moira import moira
import login as l


# SET UP MOIRA
token = l.login()
game = 'meisenheimer'

while True:
    #time.sleep(1)
    astring = moira.stock_search(token, game, 'TSLA')
    print astring['price']
    if float(astring['price']) >= 205:
        print 'yes, selling 100 shares'
        moira.order(token, 'meisenheimer', 'Sell', 'STOCK-XNAS-TSLA', 100)
    else:
        print 'no'
