# Week 6: User Interface Enhancement
# Learning Objective: Improve the user interface and user experience

# Requirements:
# Create a more polished UI using CSS framework
# Implement pagination for separating small chunks of data
# Add search functionality to filter articles
# Consolidate your work from KC1 - KC5 into a single application
# Ensure your README includes set up instructions, description, and a visual of your application in action including your database

# Compound Work: Enhance user interaction with stored data

from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import json
import sqlite3
from datetime import datetime

load_dotenv()

try:
    unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
except BaseException:
    print("Could not authenticate connection to Unsplash API.")

app = Flask(__name__)


def get_works(tag):
    try:
        r = requests.get(
            "https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=revised_at&include_work_search%5Brating_ids%5D%5B%5D=10&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id={id}".format(
                id=tag
            )
        )
        soup = BeautifulSoup(r.content, "html.parser")
        list = soup.find("ol", class_="work")
        # search_query = soup.find("h2").get_text()
        works = [x.get_text().replace("\n", "") for x in list.find_all("h4")]
        # titles.append(search_query)
        # debug = [tag, search_query]
        return works
    except BaseException:
        return {"status": 404, "message": "Sorry, that's not a valid tag."}


def get_image(tag):
    response = requests.get(
        "https://api.unsplash.com/photos/random/?topics={topic}&client_id={key}".format(
            topic=tag, key=unsplash_api_key
        )
    )
    if response.status_code == 200:
        data = response.json()
        image = {
            "author": data["user"]["name"],
            "alt": data["alt_description"],
            "url": data["urls"]["small"],
        }
        return image
    else:
        return {"status": 404, "message": "Could not get photo."}


# Store scraped data in a SQL-related database
def create_database(tag):
    # try:
    works = get_works(tag)
    image = get_image(tag)
    conn = sqlite3.connect("kc.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS works""")
    c.execute(
        """CREATE TABLE IF NOT EXISTS works (id INTEGER PRIMARY KEY, description VARCHAR(1000))"""
    )
    print("created works table")
    for work in works:
        c.execute("INSERT INTO works (description) VALUES (?)", (work,))
    print("added work to works table")
    conn.commit()
    conn.close()


# except:
# print("Could not create database.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        data = request.form.get("tag")
        create_database(data)
        conn = sqlite3.connect("kc.db")
        c = conn.cursor()
        c.execute("SELECT * FROM works")
        works = c.fetchall()
        image = get_image(data)
        print(image)
        return render_template("index.html", works=works, image=image)


if __name__ == "__main__":
    app.run()
