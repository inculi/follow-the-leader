import re
import json
import moira
import time
import requests
import os
from moira import moira
from bs4 import BeautifulSoup

def login():
    filename = os.path.expanduser('~/user.txt')
    fileout = []
    out = []
    username = ''
    password = ''
    #Check if file exists, if not, create one
    if not os.path.isfile(filename):
        print "File not found, creating file in " + filename
        open(filename, 'w').close()

    #Check if file is empty
    if os.stat(filename).st_size == 0:
        print "Empty user file, please enter your usrename and password in the file."
        exit()
    else:
        f = open(filename)
        for line in iter(f):
            fileout.append(line)
        f.close()
        for x in range(0, len(fileout)):
            out.append(fileout[x].strip())
        username = out[0]
        password = out[1]
        token = moira.get_token(username, password)
        return token
