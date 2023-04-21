# from covidai.auth import authenticate_with_azure
# from covidai.common.database import SqlServerDatabaseEngine
# from covidai.common.experimental import get_and_format_data
import requests
import sqlite3
import os
import matplotlib.pyplot as plt 

def get_data():

    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)
    data = response.json()
    yugioh_list = []
    for item in data['data']:
        yugioh_table = {} 
        yugioh_table['id'] = item['id']
        yugioh_table['name'] = item['name']
        yugioh_table['type'] = item['type']
        yugioh_table['desc'] = item['desc']
        yugioh_list.append(yugioh_table)

    return yugioh_list
    

def print_table(cur):
    cur.execute("SELECT * FROM YuGiOh")
    res = cur.fetchall()
	# for row in res:
	# 	print(row, '\n')

    

def make_tables(data, cur, con): 
    cur.execute('CREATE TABLE IF NOT EXISTS YuGiOh (id INTEGER PRIMARY KEY, name TEXT, type TEXT, desc TEXT)')
    added = 0 
    for entry in data: 
        cur.execute('SELECT * FROM YuGiOh WHERE id = ?', (entry['id'],))
        id_exists = cur.fetchone()
        if id_exists is None:
            cur.execute('INSERT OR IGNORE INTO YuGiOh (id, name, type, desc) VALUES (?,?,?,?)', (entry['id'], entry['name'], entry['type'], entry['desc']))
            added += 1
        if added > 99:
            break
    con.commit()
    return data
    

     

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path+'/FinalDatabase.db')
    cur = con.cursor()
    data = get_data()
    make_tables(data, cur, con)


main()