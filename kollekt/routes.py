from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm
from .Components.Community import Community
from .User import User
# from .models import User, db
import hashlib

test_communities = [Community("Watches", "And other timekeeping devices"),
                    Community("Trading Cards", "Baseball! Pokemon! You name it!"),
                    Community("Rocks", "Naturally formed or manually cut")]
test_user = User(1234, "test@test.com", False)


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


@app.route("/community/<community_name>", methods=['GET', 'POST'])
def communityPage(community_name):
    community = None
    for i in test_communities:
        if community_name == i.getName():
            community = i
    if request.method == 'POST':
        if request.form['join'] == 'Join Community':
            community.addUser(test_user)
        elif request.form['join'] == 'Leave Community':
            community.removeUser(test_user)
    return render_template('community.html', community=community, user=test_user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username="Test", email="test@test.com", password="1234password")
        db.session.add(user)
        db.session.commit()
        flash('registered', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
