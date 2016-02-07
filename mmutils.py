from bs4 import BeautifulSoup
import requests
import mmutils as mm

"""

    This is the utilities file, in which useful functions we need to use can be
    reused.

"""

def appendData(startColumn, finishColumn, listName, dataType, inputUrl):
    """
        Use bs4 to extract data from given table columns.
    """
    # basic string with no float() or optional replacements
    r = requests.get(inputUrl)
    soup = BeautifulSoup(r.content, "html.parser")

    if dataType == 'str':
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            data_column = row.findAll('td')[startColumn:finishColumn]
            for item in data_column:
                listName.append(item.text.replace("\t", "").replace("\r", "").replace("\n", ""))

    # money string with dollar signs and commas
    if dataType == 'money':
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            data_column = row.findAll('td')[startColumn:finishColumn]
            for item in data_column:
                listName.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("$","").replace(",","")))

    # percentages
    if dataType == 'percent':
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            data_column = row.findAll('td')[startColumn:finishColumn]
            for item in data_column:
                listName.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace("%","").replace(",","")))

    # number
    if dataType == 'float':
        for row in soup.findAll('table')[0].tbody.findAll('tr'):
            data_column = row.findAll('td')[startColumn:finishColumn]
            for item in data_column:
                listName.append(float(item.text.replace("\t", "").replace("\r", "").replace("\n", "").replace(",","")))

def getConsecutiveDays(url):
    # set up constants
    positives = 0
    negatives = 0
    zeroes = 0

    # set up bs4
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    dayReturns = []

    # manipulate data
    mm.appendData(6, 7, dayReturns, 'percent', url)
    # for x in xrange(0,int(len(dayReturns)-1)):
    #     print (dayReturns[x] - dayReturns[x+1])
    #
    # print("==========")
    for x in xrange(0,int(len(dayReturns)-1)):
        if (dayReturns[x] - dayReturns[x+1]) < 0:
            negatives+=1
        if (dayReturns[x] - dayReturns[x+1]) > 0:
            positives+=1
        elif (dayReturns[x] - dayReturns[x+1]) == 0:
            zeroes+=1
    numerator = float(len(dayReturns) + positives - negatives)
    denominator = float((2 * len(dayReturns)) + zeroes)
    return (numerator / denominator) * 100

def printAll(variable):
    for item in variable:
        print item
