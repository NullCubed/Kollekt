from flask import Flask
from flask import Blueprint

app = Flask(__name__)


@app.route("/")
def hello():
    return f"Welcome to Kollekt!<br>Created by Garrett McGhee, Parker Gagliano, Trent Salas, Will Pridgen"

