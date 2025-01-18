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

# Write a script to scrape news articles from a website (e.g., CNN, BBC)
def get_news():
    r = requests.get("https://www.wtvr.com/")
    soup = BeautifulSoup(r.content, "html.parser")
    headlines = [x.get_text() for x in soup.find_all("h3", class_="ListItem-title")]
    # print(headlines)
    return headlines


app = Flask(__name__)


@app.route("/")
def main():
    headlines = get_news()
    html = ["<p>{text}</p>".format(text=x) for x in headlines]
    return "<p>Here is the content.</p><div>{html}</div>".format(html="".join(html))


get_news()
