from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello():
    return f"Welcome to Kollekt!<br>Created by Garrett McGhee, Parker Gagliano, Trent Salas, William Pridgen, and Josh Mertz."

