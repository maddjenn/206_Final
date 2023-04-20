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
		if count > 25:
			break
	conn.commit()

# Printing all entries in Counties in database; used for debugging 
def print_table(cur):
	cur.execute("SELECT * FROM Countries")
	res = cur.fetchall()
	for row in res:
		print(row, '\n')

def calculate(cur):
	# Create an empty dictioanry to unload from FinalDatabase.db
	db =  {}
	cur.execute("SELECT * FROM Countries")
	res = cur.fetchall()

	# Add value which calculates survival rates 
	for row in res:
		db[row[0]] = (row[1], row[2], ((row[1] - row[2])/row[1]) * 100)

	# Create new dictionary organized ascending by country:survival rate 
	ordered_db = {}
	for country in db.keys():
		ordered_db[country] = ((db[country][0] - db[country][1])/db[country][0]) * 100
	ordered_db = dict(sorted(ordered_db.items(), key=lambda x:x[1]))

	# Return ordered dict for visualizing and writing 
	return ordered_db

def visualize(data): 

	# Gather lists of countries and survival rates from ordered data 
	countries = data.keys()
	survivals = []
	for country in data.keys():
		survivals.append(data[country])

	# Create bar plot (w opacity for coolness)
	plt.bar(countries, survivals, alpha = 0.3)

	# Label axes 
	plt.title("COVID-19 Survival Rates by Country")
	plt.xlabel("Countries")
	plt.ylabel("Survival Rate (Cases - Deaths)/Cases")
	
	# Organize x axis ticks to fit 90 degree rotation with font size 5 
	plt.xticks(np.arange(len(countries)), countries, rotation=90)
	plt.tick_params(axis='x', which='major', labelsize=5)

	# Organize y axis ticks to begin ~ 95%, dependent on data 
	plt.ylim([min(survivals) - .5, 100]) 

	plt.tight_layout()

	# Save and display 
	plt.savefig("COVIDSoup_Visualization.png")
	plt.show()


def calculate_and_write(file, data):
	countries = list(data.keys())
	survivals = list(data.values())

	with open(file, 'w') as f:
		# Print information 
		f.write("Using information gathered from a public COVID-19 tracking database, we consolidated data on the total listed COVID-19 cases and deaths per country.\n")
		f.write("With this data, we were able to approximate COVID-19 survival rates per country.\n")
		f.write("Here are some statistics gathered using that data:\n\n")

		# Calculate mean, median, and standard deviation of data 
		f.write(f'The average survival rate is {mean(survivals)}%, with median of {median(survivals)}% and stdev of {stdev(survivals)}.\n\n')

		# Perform calculations on country with highest survival rate  
		f.write(f'The country with the highest survival rate is {countries[len(countries) - 1]} with a survival rate of {data[countries[len(countries) - 1]]}%. ')
		f.write(f"{countries[len(countries) - 1]}'s survival rate is about {abs(mean(survivals) - data[countries[len(countries) - 1]])}% away from the mean.\n\n")

		# Perform calculations on country with lowest survival rate  
		f.write(f'The country with the lowest survival rate is {countries[0]} with a survival rate of {data[countries[0]]}%. ')
		f.write(f"{countries[0]}'s survival rate is about {abs(mean(survivals) - data[countries[0]])}% away from the mean.\n")
		
		


	


def main():
    # Get current pathname and use to connect to FinalDatabase.db 
    path = os.path.dirname(os.path.abspath(__file__))
    # print(path) # print for debugging 
    c = sqlite3.connect(path+'/FinalDatabase.db')
    
	# Use url and bs4 to gather data 
    url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'
    data = get_data(url) # store table data in variable 
    make_table(c.cursor(), c, data) # write table data to database 
    # print_table(c.cursor()) # print table for debugging 
    data = calculate(c.cursor()) # store ordered {country: survival rate} dict for calculations
    visualize(data) # visualize data using matplotlib 
    calculate_and_write("COVIDSoup_Calculations.txt", data) # perform calculations on data, write out to .txt file
	
    
main()