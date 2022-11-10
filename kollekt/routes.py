from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import RegistrationForm, LoginForm, ItemAddForm, createCommunityForm, deleteCommunityForm
# from .Components.Community import Community
# from .Components.Collection import CollectionItem

from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Communities, db


# test_communities = [Community("Watches", "And other timekeeping devices"),
#                     Community("Trading Cards", "Baseball! Pokemon! You name it!"),
#                     Community("Rocks", "Naturally formed or manually cut")]

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
    # TEST CODE ONLY I PUT INTO EMPTY ROUTE FOR NOW TO SHOW HOW IT WORKS
    #community = Communities.query.filter_by(id=2).first()
    #testcommunity = Communities.query.filter_by(id=1).first()
    # print(community)
    # community.users_in_communities.append(current_user)
    # print(community.users_in_communities[0].username)
    # print(testcommunity.users_in_communities[0].username)

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
        flash(f'Login successful', 'success')
        return redirect(url_for('home'))

    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user, remember=True)
            flash(f'Login successful {user.__repr__()}', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong Password", "Danger")
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route("/item")
def itemPage():
    return render_template('item.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username = form.username.data
    password = form.password.data
    email = form.email.data

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        eml = User.query.filter_by(email=email).first()
        if not user and not eml:
            user = User(username, password, email)
        elif user:
            flash("Username already taken", "Danger")
            return redirect(url_for('register'))
        elif email:
            flash("Email already used", "Danger")
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash(user.__repr__(), 'success')
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


@app.route("/adminpage", methods=['GET', 'POST'])
def adminpage():
    form = createCommunityForm()
    delform = deleteCommunityForm()
    allCommunities = Communities.query.all()
    if form.validate_on_submit():
        checkCommunity = Communities.query.filter_by(
            name=form.name.data).first()
        if checkCommunity:
            flash("Community already exists", "Danger")
            return redirect(url_for('adminpage'))
        else:
            community = Communities(name=form.name.data,
                                    desc=form.description.data)
            db.session.add(community)
            db.session.commit()
        flash(f"Community Created {community.name}", "success")
        return redirect(url_for('adminpage'))

    if delform.validate_on_submit():
        checkCommunity = Communities.query.filter_by(
            name=delform.name.data).first()
        if checkCommunity:
            db.session.delete(checkCommunity)
            db.session.commit()
            flash(f"Community Deleted {checkCommunity.name}", "success")
            return redirect(url_for('adminpage'))
        else:
            flash("Community does not exist", "Danger")
            return redirect(url_for('adminpage'))
    return render_template('adminpage.html', form=form, delform=delform, allCommunities=allCommunities)
