from flask import Flask
from flask import render_template
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b66a51843834a779d312d77e718b181'
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data, password=form.password.data)
        # db.session.add(user) added  in user class
        # db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=1)
