# from covidai.auth import authenticate_with_azure
# from covidai.common.database import SqlServerDatabaseEngine
# from covidai.common.experimental import get_and_format_data
import requests
import sqlite3
import os

def get_covidapi_data():
    covid_dic = {}
    url = "https://api.covidtracking.com/v1/us/daily.json"
    response = requests.get(url)
    data = response.json()
    # print(data)

    general_data_table = []
    hospital_data_table = []
    for item in data:
        general_data = {} 
        general_data['date'] = item['date']
        general_data['states'] = item['states']
        general_data['positive'] = item['positive']
        general_data['pending'] = item['pending']
        general_data['negative'] = item['negative']
        general_data['death'] = item['death']
        general_data['totalTestResults'] = item['totalTestResults']
        general_data_table.append(general_data)

        hospital_data = {}
        hospital_data['date'] = item['date']
        hospital_data['hospitalized'] = item['hospitalized']
        hospital_data['hospitalizedCurrently'] = item['hospitalizedCurrently']
        hospital_data['hospitalizedCumulative'] = item['hospitalizedCumulative']
        hospital_data['hospitalizedIncrease'] = item['hospitalizedIncrease']
        hospital_data['positiveIncrease'] = item['positiveIncrease']
        hospital_data['negativeIncrease'] = item['negativeIncrease']
        hospital_data['totalTestResultsIncrease'] = item['totalTestResultsIncrease']
        hospital_data_table.append(hospital_data)

    # print(general_data_table, hospital_data_table)
    return general_data_table, hospital_data_table

def make_tables(general_data, hospital_data, cur, con): 
    cur.execute('CREATE TABLE IF NOT EXISTS generalData (date INTEGER PRIMARY KEY, states TEXT, positive INTEGER, negative INTEGER, pending INTEGER, death INTEGER, totalTestResults INTEGER)')
    general_added = 0 
    for entry in general_data: 
        date = entry['date']
        cur.execute('SELECT * FROM generalData WHERE date = ?', (date,))
        date_exists = cur.fetchone()
        if date_exists is None:
            cur.execute('INSERT OR IGNORE INTO generalData (date, states, positive, negative, pending, death, totalTestResults) VALUES (?,?,?,?,?,?,?)', (date, entry['states'], entry['positive'], entry['negative'], entry['pending'], entry['death'], entry['totalTestResults']))
            general_added += 1
        if general_added > 24:
            break
    con.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS hospitalData (date INTEGER PRIMARY KEY, hospitalized INTEGER, hospitalizedCurrently INTEGER, hospitalizedCumulative INTEGER, hospitalizedIncrease INTEGER, positiveIncrease INTEGER, negativeIncrease INTEGER, totalTestResultsIncrease INTEGER)')
    hospital_added = 0 
    for entry in hospital_data: 
        date = entry['date']
        cur.execute('SELECT * FROM hospitalData WHERE date = ?', (date,))
        date_exists = cur.fetchone()
        if date_exists is None:
            cur.execute('INSERT OR IGNORE INTO hospitalData (date, hospitalized, hospitalizedCurrently, hospitalizedCumulative, hospitalizedIncrease, positiveIncrease, negativeIncrease, totalTestResultsIncrease) VALUES (?,?,?,?,?,?,?,?)', (date, entry['hospitalized'], entry['hospitalizedCurrently'], entry['hospitalizedCumulative'], entry['hospitalizedIncrease'], entry['positiveIncrease'], entry['negativeIncrease'], entry['totalTestResultsIncrease']))
            hospital_added += 1
        if hospital_added > 24:
            break

    con.commit()





def print_table(cur):
	cur.execute("SELECT * FROM hospitalData")
	res = cur.fetchall()
	for row in res:
		print(row, '\n')

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path+'/FinalDatabase.db')
    cur = con.cursor()
    general_data_table, hospital_data_table = get_covidapi_data()
    make_tables(general_data_table, hospital_data_table, cur, con)
    # print_table(cur)


main()