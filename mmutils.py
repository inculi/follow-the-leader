from bs4 import BeautifulSoup
import requests

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
