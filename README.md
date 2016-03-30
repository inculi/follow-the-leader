# Follow the Leader

Greetings, and welcome to the lastest installment of Robert and James's journey to employ technology for personal monetary gain. What, did you expect us to use this to build wells in Africa? Maybe in another project...  

Anways, **what is the purpose of this project**? "Follow the Leader" is a bit of a thought experiment wherein investing is examined through the looking-glass of game theory. The thought is that if we find the most successful players within Marketwatch.com's 30,000 public games, we can examine their strategies to construct a fool-proof portfolio.  

**How does it work**? We scrape the most populated games on marketwatch, and store basic information about users– starting with their overall percent returns. By scanning the top 150 most populated games, we can find a pool of around 3000 users. Of these users, about 1000 have decent returns. Of these users, about 500 are actively making trades. From here, it gets more difficult– though, arguably more fun as well. A few more self-designed ranking algorithms are employed here, including building a point system weighted in four categories: two sections dedicated to performance and prudence, and two sections dedicated to player activity and consistency.  

## Installation
You should have python installed (and its package manager, "pip").

### Dependencies
- Anaconda for python 2.7
	- download from their [website](https://www.continuum.io/downloads)
- BeautifulSoup4
	- `pip install beautifulsoup4`
- Requests
	- `pip install requests`
- Moira
	- download make-money, and navigate inside its directory (`cd ~/Downloads/make-money` or whatever it is).
	- `git clone https://github.com/brandonwu/moira.git`
- Numpy
	- `conda install numpy` *note: I don't remember why I recommended installing this. I don't think we even use this... You may want to install it anyway just to be safe...*
- Pandas
	- `conda install pandas`
- A decent internet connection
	- you will most likely be making tens of thousands of page visits. Assuming no one buys/sells anything, you'll be making easily over 2,000 page calls a day... Not including the few thousand every time you scan the top 100+ games.

## Usage
You can begin scanning marketwatch games by using:  
`python gamescan.py`  

This shall return a few .csv files, each ranked differently, but with the final file (players.csv) showing you our preffered top 50 players. This entire scanning process should take a little over 30 minutes, provided that you have decent internet access. After all, it is accessing multiple pages for each user in order to scrape data crucial to the ranking process. If you open the file in excel (any text interpreter works, but won't always look as nice), look at the column labeled "mmScore". This is the final score for a user, taking into account all rankings. The max score is 1000, assuming they rank #1 in all aspects. Use this lineup to decide whose trades you wish to copy. Remeber to take in mind, however, that some marketwatch games have a minimum price. If a user's strategy calls for buying penny stocks, you may want to monitor someone else (you can examine their tendencies by visiting their transactionsUrl).

Once you have decided on a user to monitor (eventually this will automatically follow the top 50 users... ) visit the very end of receipt.py. In here, you will find a `while True:` statement looping the function `copyTrades(url)`. Insert the transactionUrl of the player you wish to monitor. Example:

```python
While True:
    copyTrades("http://www.marketwatch.com/game/moiratestone/portfolio/transactionhistory?name=Sheikh%20Hamdan%20bin%20Mohammed%20Al%20Maktoum&p=895646")
    time.sleep(30) # to be nice to their servers
```

Now, make sure that your holdings.log is cleared...

```fish
⚓  ~/D/P/follow-the-leader  master ⚑  rm holdings.log
⚓  ~/D/P/follow-the-leader  master ⚑  touch holdings.log
```

All that's left to do is for it to run:
```fish
⚓  ~/D/P/follow-the-leader  master ⚑  python receipt.py
```

You can close it at the end of market time, so long as you remember to start it back up before the market re-opens. You may also want to rinse-and-repeat every so often with a fresh gamescan (to get a new user to follow).

Best of luck!

## Credits
To [James](http://github.com/jaykm/) for making the code that finds game urls– and nothing else. Granted, I shouldn't have originally given you the task of working on transactions. Working on that part has been like solving a jigsaw puzzle made of four-dimensional sand. While skydiving. Blindfolded.

Oh, holy team of marketwatch.com... Praise and blessings be to you for your patience with me. Thank you for not being like google and banning my IP after a few screen-scrapes. If you come across this and decide to start banning IPs, could you please give me access to some sort of API so I can keep scanning? I'd hate to resort to slow proxies. Think of the children. Think of the child that has worked on this program since January 2016. Do you have any idea how difficult it is to write a program that can only be debugged during school hours? Granted, this is more fun than analyzing *Ode on a Grecian Urn*. Was I correct to use italics? Or are poems denoted by quotes? If only I had payed attention in English class... Oh wait. I was working on this...

----
**TL;DR**: This program allows users to combine the best strategies of the best players on the MarketWatch site in order for us to become the best.