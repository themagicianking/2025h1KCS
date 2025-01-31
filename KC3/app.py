# Week 3: Form Validation and Basic CRUD Operations
# Learning Objective: Implement form handling and basic CRUD operations

# Requirements:
# Create HTML forms for user input (search queries, article selection)
# Implement client-side form validation
# Develop routes for CRUD operations (create, read, update, delete)
# Store data in SQL-related database

# Compound Work: Integrate web scraping from previous weeks with form handling

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_works():
    r = requests.get("https://archiveofourown.org/tags/Art/works")
    soup = BeautifulSoup(r.content, "html.parser")
    works = soup.find("ol", class_="work")
    titles = [x.get_text() for x in works.find_all("h4")]
    return titles


@app.route("/")
def main():
    works = get_works()
    try:
        return render_template("index.html", works=works)
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run()
