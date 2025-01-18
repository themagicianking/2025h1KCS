# Week 1: E-commerce Product Aggregator Project Setup and Basic Web Scraping

# Learning Objective: Set up a Python Flask project and perform basic web scraping

# Create a new Flask project
# Install required packages (Flask, BeautifulSoup, requests)
from flask import Flask
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime


app = Flask(__name__)

# Write a script to scrape news articles from a website (e.g., CNN, BBC)
def get_news():
    r = requests.get("https://www.wtvr.com/")
    soup = BeautifulSoup(r.content, "html.parser")
    headlines = [x.get_text() for x in soup.find_all("h3", class_="ListItem-title")]
    return headlines

# Store scraped data in a SQL-related database
def create_database():
    headlines = get_news()
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS news''')
    c.execute('''CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, headline TEXT)''')
    print("created news table")
    for headline in headlines:
        c.execute('INSERT INTO news (headline) VALUES (?)', (headline,))
    print("added headlines to news table")
    conn.commit()
    conn.close()


@app.route("/")
# Create a simple web interface to display stored headlines
def main():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news')
    news = c.fetchall()
    conn.close()
    rows = []
    rows.append("""<table><tr><th>Article ID</th><th>Headline<th></tr>""")
    for article in news:
        rows.append("""<tr><td>{ID}</td><td>{headline}</td></tr>""".format(ID=article[0], headline=article[1]))
    rows.append("""</table>""")
    return "".join(rows)


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
