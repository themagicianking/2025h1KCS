# Week 1: E-commerce Product Aggregator Project Setup and Basic Web Scraping

# Learning Objective: Set up a Python Flask project and perform basic web scraping

# Requirements:
# Store scraped data in a SQL-related database
# Create a simple web interface to display stored headlines

# Compound Work: None yet

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

def create_database():
    headlines = get_news()
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, headline TEXT)''')
    print("created news table")
    for headline in headlines:
        c.execute('INSERT INTO news (headline) VALUES (?)', (headline,))
    print("added headlines to news table")
    conn.commit()
    conn.close()


@app.route("/")
def main():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news')
    news = c.fetchall()
    conn.close()
    print("running")
    # news = "hi"
    return "<p>{news}</p>".format(news=news)
    # headlines = get_news()
    # html = ["<p>{text}</p>".format(text=x) for x in headlines]
    # return "<p>Here is the content.</p><div>{html}</div>".format(html="".join(html))


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
