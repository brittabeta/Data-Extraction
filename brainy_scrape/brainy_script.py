# script to obtain: motivational quotes from brainyquote.com

# terminal directions for use
# $ pip install lxml #install lxml for parsing
# $ pip install openpyxl #install to write dataframe to excel file
# $ pip install cloudscraper #install to obtain html from website
# $ cd brainy_scrape # go here to execute script
# $ python3 brainy_script.py # execute to obtain excel file of motivational brainy quotes

from cloudscraper import create_scraper # import to create scraper object
from bs4 import BeautifulSoup # import to parse response
import pandas as pd # import for working with dataframes

scraper = create_scraper() # create scraper object

alist = [] # define function to obtain author target items, create dictonary of items, then dict to list
def getauthor(a):
    i = 0
    for item in a:
        aitem = a[i]
        author = aitem.text
        alink = aitem['href']
        aitems = {'author': author,
                'author_link': alink}
        alist.append(aitems)
        i += 1

qlist = [] # define function to obtain quote target items, create dictonary of items, then dict to list
def getquote(q):
    j = 0
    for itemq in q:
        qitem = q[j]
        quote = qitem.text.strip()
        qlink = qitem['href']
        qitems = {'quote': quote,
                'quote_link': qlink}
        qlist.append(qitems)
        j += 1

# pagination through pages 1-5 = all pages scrapped
alist = [] 
qlist = []
for n in range(1, 6):
    response = scraper.get(f'https://www.brainyquote.com/topics/motivational-quotes_{n}')
    soup = BeautifulSoup(response.text, 'lxml')
    a = soup.select('body main .oncl_a')
    q = soup.select('body main .b-qt')
    getauthor(a)
    getquote(q) 

author_df = pd.DataFrame(alist) # create dataframe from author list
quote_df = pd.DataFrame(qlist) # create dataframe from quote list
df = quote_df.join(author_df) # merge, how = left by default, into one dataframe

brainy_quotes = df.to_excel('brainy_quotes.xlsx', index = False) # export dataframe as excel file