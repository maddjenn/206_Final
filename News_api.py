import sqlite3
import os
from newsapi import NewsApiClient

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_newsapi_data(query):
    news_dic = {}
    article_list = []
    news_api = NewsApiClient(api_key='1e90d81518524f51a9aba8405923a800')
    data = news_api.get_everything(q=query, language='en')
    for article in data['articles']:
        article_dic = {}
        article_dic['title'] = article['title']
        if article['author'] == None:
            article['author'] = "None Provided"
        article_dic['author'] = article['author']
        article_dic['description'] = article['description']
        article_list.append(article_dic)
    news_dic['articles'] = article_list

    return news_dic    
    
def make_articles_table(cur, conn, data):
    cur.execute('CREATE TABLE IF NOT EXISTS Articles (title TEXT, author TEXT, description TEXT)')
    articles_added = 0
    for article in data['articles']:
        if articles_added < 25:
            title = article['title']
            author = article['author']
            description = article['description']
            cur.execute('SELECT * FROM Articles WHERE title = ?', (title,))
            existing_article = cur.fetchone()
            if existing_article is None:
                cur.execute('INSERT INTO Articles (title, author, description) VALUES (?,?,?)', (title, author, description))
                articles_added += 1
    conn.commit() 

     

def main():
    cur, conn = open_database('FinalDatabase.db')
    #covid_data = get_newsapi_data("covid")
    disease_data = get_newsapi_data('disease')
    #make_articles_table(cur, conn, covid_data)
    make_articles_table(cur, conn, disease_data)


main()
