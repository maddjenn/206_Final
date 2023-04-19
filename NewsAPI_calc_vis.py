import sqlite3
import matplotlib.pyplot as plt
import os

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_calculations(cur, conn):
    results = {}
    cur.execute("SELECT COUNT(*) FROM Articles WHERE title LIKE '%covid%'")
    results['covid_titles'] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM Articles WHERE title NOT LIKE '%covid%'")
    results['non_covid_titles'] = cur.fetchone()[0]
    conn.close()
    return results

def write_file(filename, dic):
    with open(filename, 'w') as file:
        file.write('For the News API calculations, we decided that it would be interesing to see how many titles include the word Covid.\n''We retrieved 200 articles about diseases, in general, and covid.\n' 'Below are the answers: \n' )
        file.write(f'The number of titles that include covid is: {dic["covid_titles"]}. \n')
        file.write(f'The number of titles that do not include covid is: {dic["non_covid_titles"]}.\n')

def visualization(dic):
    labels = ['Covid-mentioning Titles', 'Non-Covid-mentioning Titles']
    counts = [dic['covid_titles'], dic['non_covid_titles']]
    plt.bar(labels, counts)

    plt.title('Article Titles')
    plt.xlabel('Title Type')
    plt.ylabel('Number of Titles')

    plt.show()


def main():
    cur, conn = open_database('FinalDatabase.db')
    results = get_calculations(cur, conn)
    write_file('NewsAPI_Calculations.txt', results)
    visualization(results)
    

main()