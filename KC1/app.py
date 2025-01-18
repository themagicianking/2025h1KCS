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


# Write a script to scrape news articles from a website (e.g., CNN, BBC)
def get_news():
    r = requests.get("https://richmond.com/")
    print(r)


app = Flask(__name__)


@app.route("/")
def main():
    return "<p>Placeholder text</p>"
