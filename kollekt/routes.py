from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm
from kollekt.models import User
import hashlib


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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #user = User()
        # db.session.add(user) added  in user class
        # db.session.commit()
        flash('registered', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
