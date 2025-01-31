# Week 3: Form Validation and Basic CRUD Operations
# Learning Objective: Implement form handling and basic CRUD operations

# Requirements:
# Create HTML forms for user input (search queries, article selection)
# Implement client-side form validation
# Develop routes for CRUD operations (create, read, update, delete)
# Store data in SQL-related database

# Compound Work: Integrate web scraping from previous weeks with form handling

from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "Hello World"


if __name__ == "__main__":
    app.run()
