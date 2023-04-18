from covidai.auth import authenticate_with_azure
from covidai.common.database import SqlServerDatabaseEngine
from covidai.common.experimental import get_and_format_data
import requests
import sqlite3

def get_covidapi_data():
    covid_dic = {}
    url = "https://covidtracking.com/data/api/version-2"
    headers = {
        "Authorization": "Bearer <WHATEVER THE FUCK MY API KEY IS I CANT FIND IT >"
    }
    params = {
        "limit": 25
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    for item in data['results']:
        item_dic = {}
        item_dic['name'] = item['name']
        item_dic['value'] = item['value']
        item_dic['unit'] = item['unit']
        covid_dic[item['id']] = item_dic
    return covid_dic

#	tests.pcr.total


def fetch_covid_data():
    url = 'https://api.covidtracking.com/v1/us/daily.json'
    response = requests.get(url)
    data = response.json()

    conn = sqlite3.connect('covid_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS daily_stats
                 (id INTEGER PRIMARY KEY, date INTEGER, cases INTEGER, deaths INTEGER, tests INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS race_ethnicity
                 (id INTEGER PRIMARY KEY, date INTEGER, race TEXT, cases INTEGER, deaths INTEGER)''')

    for item in data:
        # insert into daily_stats table
        c.execute('''INSERT OR IGNORE INTO daily_stats (id, date, cases, deaths, tests)
                     VALUES (?, ?, ?, ?, ?)''', (item['date'], item['date'], item['positive'], item['death'], item['total']))
        
        # insert into race_ethnicity table
        for race_item in item['raceEthnicity']:
            c.execute('''INSERT OR IGNORE INTO race_ethnicity (id, date, race, cases, deaths)
                         VALUES (?, ?, ?, ?, ?)''', (item['date'], item['date'], race_item['name'], race_item['cases'], race_item['deaths']))
    
    conn.commit()
    conn.close()
