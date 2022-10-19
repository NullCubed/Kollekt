from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/userProfile")
def userProfile():
    return render_template('test.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/userSettings")
def userSettings():
    return render_template('settings.html')


@app.route("/community")
def communityPage():
    return render_template('community.html')


if __name__ == '__main__':
    app.run(debug=1)
