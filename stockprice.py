import re
import json
import requests
from bs4 import BeautifulSoup

while True:
	url = "https://www.google.com/finance/info?client=ob&infotype=infoonebox&hl=en&ei=hkOgVvbXOOj7jgSXiLyIDA&q=NYSE%3AIBM&auto=1"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	all = soup.get_text()
	good_data = all.replace("\t", "").replace("\r", "").replace("\n", "")
	m = re.search('l_fix\" : \"(.+?)\"', good_data)
	if m:
	    found = m.group(1)
	print found
