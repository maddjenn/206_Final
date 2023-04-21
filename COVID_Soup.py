import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import sqlite3
import os
import numpy as np
from statistics import mean, median, stdev

def get_data(url):
	# Retrieve page HTML using Beautiful Soup 
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	# Create empty dict 
	data = {}

	td_list = soup.find_all('td')
	for i in range(0, len(td_list), 4):
		country = td_list[i].text
		confirmed = td_list[i + 1].text.replace(',', '')
		deaths = td_list[i + 2].text.replace(',', '')
		data[country] = (confirmed, deaths)
	return data 


def make_table(cur, conn, data):
	# Create or add to table with UNIQUE TEXT for country to prevent duplicates 
	cur.execute('CREATE TABLE IF NOT EXISTS Countries (country TEXT UNIQUE, confirmed INTEGER, deaths INTEGER)')

	count = 0

	# Parse through each country and insert 25 new datapoints to database 
	for country in data.keys():
		confirmed = data[country][0]
		deaths = data[country][1]

		# Check if entry within Countries in database exists where country = current country name 
		cur.execute('SELECT * FROM Countries WHERE country = ?', (country,))
		exists = cur.fetchone()
		if exists is None:
			cur.execute('INSERT OR IGNORE INTO Countries (country, confirmed, deaths) VALUES (?,?,?)', (country, confirmed, deaths))
			count += 1
		if count > 24:
			break
	conn.commit()

# Printing all entries in Counties in database; used for debugging 
def print_table(cur):
	cur.execute("SELECT * FROM Countries")
	res = cur.fetchall()
	for row in res:
		print(row, '\n')


	


def main():
    # Get current pathname and use to connect to FinalDatabase.db 
    path = os.path.dirname(os.path.abspath(__file__))
    # print(path) # print for debugging 
    c = sqlite3.connect(path+'/FinalDatabase.db')
    
	# Use url and bs4 to gather data 
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    data = get_data(url) # store table data in variable 
    make_table(c.cursor(), c, data) # write table data to database 
	
    
main()