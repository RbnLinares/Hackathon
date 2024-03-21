from bs4 import BeautifulSoup
import requests

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def detect_not_ok(text):
    return 'not ok' in text.lower()

# Example usage
ok_page_text = scrape_page('file:///path/to/ok_page.html')
not_ok_page_text = scrape_page('file:///path/to/not_ok_page.html')

print(detect_not_ok(ok_page_text)) # False
print(detect_not_ok(not_ok_page_text)) # True

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

# Example usage
# conn = create_database_connection()
# create_resources_table(conn)
# insert_resource(conn, "Antisemitism Education Resource", "https://example.com/resource")
# resources = get_resources(conn)
# print(resources)

# conn.close()

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/resources/<int:level>')
def get_resources(level):
    # Example resources based on analysis level
    resources = {
        1: ["Resource 1", "Resource 2"],
        2: ["Resource 3", "Resource 4", "Resource 5"],
        3: ["Resource 6", "Resource 7", "Resource 8", "Resource 9"]
    }
    return jsonify(resources.get(level, []))

if __name__ == '__main__':
    app.run(debug=True)
