from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm, ItemAddForm
from .Components.Collection import CollectionItem
from .models import User, db

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



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.password == form.password.data:
            flash(f'Logged into {user.id}!', 'success')
            return redirect(url_for('home'))
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
        db.session.add(user)
        db.session.commit()
        test = db.get_or_404(User, 1)
        flash(test.username+" "+test.email+" "+test.password, 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/addItem", methods=['GET', 'POST'])
def addNewCollectionItem():
    form = ItemAddForm()
    if form.validate_on_submit():
        collection_item = CollectionItem('testUser','testCommunity','testTemplate',
                                         'testPhoto',text=form.text.data,
                                         collection=form.community.data)
        text2 = form.text.data
        community2 = form.community.data
        print(text2,community2)
        return render_template("item.html", title="Your Item", item=collection_item)
    return render_template("addItem.html", title='Add Item', form=form)

5