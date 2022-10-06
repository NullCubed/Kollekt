from flask import Flask
from flask import render_template
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/userProfile")
def userProfile():
    return render_template('test.html')


@app.route("/community")
def communityPage():
    return render_template('community.html')


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=1)
