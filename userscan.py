import requests
from bs4 import BeautifulSoup

"""
    Once all the data for the top 100 games has been indexed, this shall go
    through those users to append more relevant information to their data
    profiles so that they can be ranked more accurately.
"""



performance_Dates = []
performance_Ranks = []
performance_Cash = []
performance_Cash_Int = []
performance_Margin_Cost = []
performance_Total_Equity = []
performance_Returns = []

def getPerformance(inputURL):
    url = inputURL
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")



    # [6:7] Return
    # [5:6] total equity
    # [4:5] margin cost
    # [3:4] cash Int
    # [2:3] cash
    # [1:2] rank
    # [0:1] date

    #date
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[0:1]
        for item in data_column:
            performance_Dates.append(item.text.replace("\t", "").replace("\r", "").replace("\n", ""))

    # rank
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[1:2]
        for item in data_column:
            performance_Ranks.append(item.text.replace("\t", "").replace("\r", "").replace("\n", ""))

    # cash
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[2:3]
        for item in data_column:
            performance_Cash.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$","").replace(",","")))

    # cash int
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[3:4]
        for item in data_column:
            performance_Cash_Int.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$","").replace(",","")))

    # margin cost
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[4:5]
        for item in data_column:
            performance_Margin_Cost.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$","").replace(",","")))

    # total equity
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[5:6]
        for item in data_column:
            performance_Total_Equity.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$","").replace(",","")))

    # returns
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        data_column = row.findAll('td')[6:7]
        for item in data_column:
            performance_Returns.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("%","").replace(",","")))


getPerformance("http://www.marketwatch.com/game/stock-fears/portfolio/performance?name=Dustin%20Lien&p=1354179")

for element in performance_Dates:
    print element

for element in performance_Ranks:
    print element

for element in performance_Cash:
    print element

for element in performance_Cash_Int:
    print element

for element in performance_Margin_Cost:
    print element

for element in performance_Total_Equity:
    print element

for element in performance_Returns:
    print element
#
