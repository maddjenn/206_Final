#import sqlite3
from newsapi import NewsApiClient
#import matplotlib.pyplot as plt

def get_newsapi_data(query):
    news_dic = {}
    article_list = []
    news_api = NewsApiClient(api_key='1e90d81518524f51a9aba8405923a800')
    data = news_api.get_everything(q=query, language='en')
    news_dic["total_results"] = data["totalResults"]
    for article in data['articles']:
        article_dic = {}
        article_dic['title'] = article['title']
        article_dic['author'] = article['author']
        article_dic['description'] = article['description']
        article_list.append(article_dic)
    news_dic['articles'] = article_list

    return news_dic
    
 

def main():
    data = get_newsapi_data("covid")
    #print(len(data['articles']))
    

main()
       
