import re
import json
import moira
import requests
from moira import moira
from bs4 import BeautifulSoup

username = 'labresearch9@gmail.com'
password = 'qazwsxedcrf'
game = 'meisenheimer'





token = moira.get_token(username, password)
portfolio = moira.get_portfolio_data(token, game)
print portfolio
print portfolio['net_worth']

mynet = portfolio['net_worth']

"""
price = 7.45
my_bal = 2000000.0
his_bal = 265000.0
shares_he_bought = 2022
print price * (my_bal / his_bal) * shares_he_bought
"""
