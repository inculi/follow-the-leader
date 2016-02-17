# make-money

Greetings, and welcome to the lastest installment of Robert and James' journey to employ technology for personal monetary gain. What, did you expect us to use this to build wells in Africa? Maybe in another project...  

Anways, **what is the purpose of this project**? Make-money is a bit of a thought experiment wherein investing is examined through the looking-glass of game theory. The thought is that if we find the most successful players within Marketwatch.com's 30,000 public games, we can examine their strategies to construct a fool-proof portfolio.  

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
	- `conda install numpy`
- Pandas
	- `conda install pandas`

## Usage
You can begin scanning marketwatch games by using:  
`python gamescan.py`  

This shall return a few .csv files, each ranked differently, but with the final file showing you our preffered top 50 players. This entire scanning process should take a little over 30 minutes, provided that you have decent internet access. After all, it is accessing multiple pages for each user in order to scrape data crucial to the ranking process.  

For now, that is all this program is capable of. Certain programmers are having difficulty mirroring the transactions of players *\*cough\** James *\*cough\**.

----
**TL;DR**: This program allows users to combine the best strategies of the best players on the MarketWatch site in order for us to become the best.