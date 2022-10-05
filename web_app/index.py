from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/userProfile")
def userProfile():
    return render_template('test.html')


@app.route("/community")
def userProfile():
    return render_template('community.html')


if __name__ == '__main__':
    app.run(debug=1)
