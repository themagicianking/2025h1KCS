# Week 2: Web Scraping with Authentication and Storage
# Learning Objective: Improve web scraping capabilities and store extracted data locally

# Requirements:
    # Implement login authentication for target websites
    # Handle rate limiting and anti-bot measures
    # Store scraped data in a SQL-related database
    # Create a simple web interface to display stored article summaries


# More on rate limiting here: https://upstash.com/blog/rate-limiting-with-python

# Compound Work: Build upon Week 1's scraping capabilities

# Create a new Flask project
# Install required packages (Flask, BeautifulSoup, requests)
from flask import Flask, render_template
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
    recipes = [{"title": "Title", "ingredients": ["flour", "butter", "milk"]}, "instructions": ["step one", "step two"]]
    return render_template("recipes.html", recipes=recipes)


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
