import requests
from newsapi import NewsApiClient
from textblob import TextBlob
from bs4 import BeautifulSoup
import psycopg2
import config
import random

def insert_article(conn, table_name, article):
    with conn.cursor() as cursor:
        insert_query = f"""
            INSERT INTO {table_name} (title, url, content)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (article['title'], article['url'], article['content']))
        conn.commit()

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"

def connect_to_database():
    conn = psycopg2.connect(
        dbname=config.DATABASE,
        user=config.USERNAME,
        password=config.PASSWORD,
        host=config.HOSTNAME,
        port=config.PORT
    )
    return conn

def educative_resource():
    recommended_pages = [
        "https://www.google.com/search?q=basic+information+on+antisemitism",
        "https://www.google.com/search?q=combating+antisemitism",
        "https://www.google.com/search?q=latest+on+antisemitism+2024"
    ]
    selected_page = random.choice(recommended_pages)
    print(f"Suggested Page: {selected_page}")

def store_articles_in_database(news_results, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    all_articles = newsapi.get_everything(q='Jews, Israel, Jewish community, Jewish culture, Jewish history, Antisemitism, Holocaust, Nazi',
                                          language='en',
                                          sort_by='relevancy')
    conn = connect_to_database()
    articles_list = []
    for article in all_articles['articles']:
        try:
            article_response = requests.get(article['url'])
            article_response.raise_for_status() 
            if article_response.ok:
                soup = BeautifulSoup(article_response.text, 'html.parser')
                content = soup.get_text()
                sentiment = analyze_sentiment(content)
                articles_list.append((article, sentiment))
        except requests.exceptions.HTTPError as err:
            print(f"Error al descargar el artículo: {err}")
            continue 

    if articles_list:
        random_article, sentiment = random.choice(articles_list)
        print(f'Random Article; {random_article["title"]}\nURL: {random_article["url"]}\nSentiment: {sentiment}')

        if sentiment == "positive":
            insert_article(conn, "positive_articles", random_article)
        elif sentiment == "negative":
            insert_article(conn, "negative_articles", random_article)
        else:
            insert_article(conn, "neutral_articles", random_article)

    conn.close()

    educative_resource()

# query = "Jews, Israel, Jewish community, Jewish culture, Jewish history, Antisemitism, Holocaust, Nazi"
api_key = "66145059beff4e648d9ec738e0ffb67a"
store_articles_in_database(None, api_key)
