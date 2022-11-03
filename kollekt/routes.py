from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm, ItemAddForm
from .Components.Community import Community
from .Components.Collection import CollectionItem
import hashlib
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, db

test_communities = [Community("Watches", "And other timekeeping devices"),
                    Community("Trading Cards", "Baseball! Pokemon! You name it!"),
                    Community("Rocks", "Naturally formed or manually cut")]


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/userProfile")
def userProfile():
    return render_template('test.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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
            community.addUser(current_user)
        elif request.form['join'] == 'Leave Community':
            community.removeUser(current_user)
    return render_template('community.html', community=community, user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Login successful ${current_user.email}', 'success')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            flash(f'Login successful ${current_user.email}', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong Password", "Danger")

    return render_template('login.html', title='Login', form=form)


@app.route("/item")
def itemPage():
    return render_template('item.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)

        checkUsername = User.query.filter_by(username=form.username.data).first()
        if checkUsername:
            flash("Username already taken", "Danger")
            return redirect(url_for('register'))
        checkEmail = User.query.filter_by(email=form.email.data).first()
        if checkEmail:
            flash("Email already taken", "Danger")
            return redirect(url_for('register'))

        db.session.add(user)
        db.session.commit()
        test = db.get_or_404(User, 1)
        flash(test.username + " " + test.email + " " + test.password, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/addItem", methods=['GET', 'POST'])
def addNewCollectionItem():
    form = ItemAddForm()
    if form.validate_on_submit():
        collection_item = CollectionItem('testUser', 'testCommunity', 'testTemplate',
                                         'testPhoto', text=form.text.data,
                                         collection=form.community.data)
        text2 = form.text.data
        community2 = form.community.data
        print(text2, community2)
        return render_template("item.html", title="Your Item", item=collection_item)
    return render_template("addItem.html", title='Add Item', form=form)
