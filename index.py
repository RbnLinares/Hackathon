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

    import sqlite3

def create_database():
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (level text, resource text)''')
    conn.commit()
    conn.close()

def add_resource(level, resource):
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    c.execute("INSERT INTO resources VALUES (?, ?)", (level, resource))
    conn.commit()
    conn.close()

def get_resources(level):
    conn = sqlite3.connect('resources.db')
    c = conn.cursor()
    c.execute("SELECT resource FROM resources WHERE level=?", (level,))
    resources = [row[0] for row in c.fetchall()]
    conn.close()
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