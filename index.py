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

def buscar_recursos_educativos(query):
    url = "https://www.google.com/search"
    params = {
        "q": query,
        "tbm": "isch" 
    }
    response = requests.get(url, params=params)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and "educational" in href: # Esto es solo un ejemplo, necesitarás una lógica más sofisticada
                print(f"Recurso educativo sugerido: {href}")
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
                # print(article_response.ok)
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
query = "Jews", "Israel", "Jewish community", "Jewish culture", "Jewish history"
api_key = "66145059beff4e648d9ec738e0ffb67a"
store_articles_in_database(None, api_key) 





import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    return None

def detect_not_ok_texts(soup):
    not_ok_texts = []
    # Assuming 'not ok' texts are in paragraph tags with a specific class
    for p in soup.find_all('p', class_='not-ok-text'):
        not_ok_texts.append(p.text)
    return not_ok_texts

def analyze_texts(not_ok_texts):
    # Placeholder for text analysis logic
    # This could involve natural language processing (NLP) to determine the level of the text
    # For simplicity, let's assume a basic level analysis
    levels = ['low', 'medium', 'high']
    return levels[len(not_ok_texts) % len(levels)] # Example logic

def suggest_resources(level):
    # Placeholder for fetching resources from a database
    # This could involve querying a database based on the level of the detected text
    # For simplicity, let's return a static list of resources
    resources = {
        'low': ['Resource 1', 'Resource 2'],
        'medium': ['Resource 3', 'Resource 4'],
        'high': ['Resource 5', 'Resource 6']
    }
    return resources[level]

import psycopg2

def create_database_connection():
    conn = psycopg2.connect(
        database="your_database_name",
        user="your_database_user",
        password="your_database_password",
        host="your_database_host",
        port="your_database_port"
    )
    return conn

def create_resources_table(conn):
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS resources (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT NOT NULL
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

def insert_resource(conn, title, url):
    cursor = conn.cursor()
    insert_query = "INSERT INTO resources (title, url) VALUES (%s, %s)"
    cursor.execute(insert_query, (title, url))
    conn.commit()
    cursor.close()

def get_resources(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resources")
    resources = cursor.fetchall()
    cursor.close()
    return resources

def main():
    url = 'http://example.com/fake-page'
    soup = scrape_page(url)
    if soup:
        not_ok_texts = detect_not_ok_texts(soup)
        level = analyze_texts(not_ok_texts)
        resources = suggest_resources(level)
        print(f"Suggested resources for level '{level}': {resources}")

if __name__ == "__main__":
    main()


