import requests
from newsapi import NewsApiClient
from textblob import TextBlob
from bs4 import BeautifulSoup
import psycopg2
import config

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

def educative_resource(query):
    url = "https://www.google.com/search"
    params = {
        "q": query,
    }
    response = requests.get(url, params=params)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "educational" in href: "https://www.yadvashem.org/es/education/educational-materials/video-toolbox/hevt-antisemitism.html"
            print(f"Suggested Page: {href}")
    else:
        print(f"Error al buscar recursos educativos: {response.status_code}")
def store_articles_in_database(news_results, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    all_articles = newsapi.get_everything(q='Jews, Israel, Jewish community, Jewish culture, Jewish history, Antisemitism, Holocaust, Nazi',
                                          language='en',
                                          sort_by='relevancy')
    conn = connect_to_database()
    for article in all_articles['articles']:
        try:
            article_response = requests.get(article['url'])
            article_response.raise_for_status() 
            if article_response.ok:
                print(article_response.ok)
                soup = BeautifulSoup(article_response.text, 'html.parser')
                content = soup.get_text()
                sentiment = analyze_sentiment(article_response.text)
            if sentiment == "positive":
                insert_article(conn, "positive_articles", article)
            elif sentiment == "negative":
                insert_article(conn, "negative_articles", article)
            else:
                insert_article(conn, "positive_articles", article)
        except requests.exceptions.HTTPError as err:
            print(f"Error al descargar el artículo: {err}")
            continue 

    conn.close()
query = "Jews", "Israel", "Jewish community", "Jewish culture", "Jewish history", "Antisemitism", "Holocaust", "Nazi"
api_key = "66145059beff4e648d9ec738e0ffb67a"
store_articles_in_database(None, api_key) 
