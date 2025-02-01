# Week 3: Form Validation and Basic CRUD Operations
# Learning Objective: Implement form handling and basic CRUD operations

# Requirements:
# Create HTML forms for user input (search queries, article selection)
# Implement client-side form validation
# Develop routes for CRUD operations (create, read, update, delete)
# Store data in SQL-related database

# Compound Work: Integrate web scraping from previous weeks with form handling

from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

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
        works = [x.get_text() for x in list.find_all("h4")]
        # titles.append(search_query)
        # debug = [tag, search_query]
        return {"status": 200, "works": works}
    except Exception:
        return {"status": 404, "message": "Sorry, that's not a valid tag."}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        data = request.form.get("tag")
        works = get_works(data)
        if works["status"] == 200:
            return render_template("index.html", works=works["works"])
        else:
            return render_template("index.html", error=works["message"])


if __name__ == "__main__":
    app.run()
