import requests
from textblob import TextBlob

def search_news_about_antisemitism(api_key, query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": api_key
    }
    
    response = requests.get(url, params=params)
    if response.ok:
        return response.json()
    else:
        print(f"Error al buscar noticias: {response.status_code}")
        return None

def analyze_sentiment(text):
    # Crea un objeto TextBlob con el texto del artículo
    blob = TextBlob(text)
    # Obtiene la puntuación de sentimiento del texto
    sentiment = blob.sentiment.polarity
    # Devuelve el sentimiento (positivo, negativo, neutral)
    if sentiment > 0:
        return "positivo"
    elif sentiment < 0:
        return "negativo"
    else:
        return "neutral"

def filter_positive_articles(news_results):
    positive_articles = []
    for article in news_results['articles']:
        # Descarga el contenido del artículo
        article_response = requests.get(article['url'])
        if article_response.ok:
            # Analiza el sentimiento del contenido del artículo
            sentiment = analyze_sentiment(article_response.text)
            if sentiment == "positivo":
                positive_articles.append(article)
        else:
            print(f"Error al descargar el artículo: {article_response.status_code}")
    return positive_articles

api_key = "66145059beff4e648d9ec738e0ffb67a"
# Ajusta la consulta para buscar términos positivos
query = "Jews, Israel, Jewish community, Jewish culture, Jewish history"
news_results = search_news_about_antisemitism(api_key, query)
if news_results:
    positive_articles = filter_positive_articles(news_results)
    for article in positive_articles:
        print(f"Título: {article['title']}, Sentimiento: Positivo")