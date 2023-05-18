# script to obtain: download speeds from speedtest.net

# terminal directions for use
# $ pip install lxml #install lxml for parsing
# $ pip install openpyxl #install to write dataframe to excel file
# $ pip install cloudscraper #install to obtain html from website
# $ cd speedtest # go here to execute script
# $ python3 speed_scrape.py # execute to obtain excel file of motivational brainy quotes

# collaborator: Khaliq Salawon 

# import the dependencies
from cloudscraper import create_scraper
import pandas as pd
from bs4 import BeautifulSoup

# create the create_scraper object
scraper = create_scraper()

# sent the request and parse the html with Beautifulsoup
response = scraper.get('https://www.speedtest.net/global-index')
soup = BeautifulSoup(response.text, 'lxml')

# extract the month and names
month = soup.select_one('.month').text
names = soup.select('.graph')
all_names = []
for name in names:
    all_name = name['id'].split('-')[1]
    all_names.append(all_name)

# created a new_list to store the unique names and remove dedupes
table_names = []
for i in all_names:
    if i not in table_names:
        table_names.append(i)

# read the html with pandas to get all the tables
tables = pd.read_html(response.text)

# created a new list to save the updated tables with name and month (Data Cleaning)
# drop rows with NA values, ignore_index to retain 0,1,2...index
all_tables = []
for i in range(len(tables)):
    tables[i]['Month'] = month
    tables[i]['Name'] = table_names[i]
    tables[i].drop(columns=['#', '#.1'], inplace=True, axis=1)
    tables[i].dropna(inplace=True, ignore_index=True) 
    all_tables.append(tables[i])

# looping through all_tables to save each as an excel file
for t in range(len(all_tables)):
    all_tables[t].to_excel(f'{table_names[t]}.xlsx', index=False)