from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from kollekt.forms import *
# from .Components.Community import Community
# from .Components.Collection import CollectionItem

from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Communities, Collections, Posts, db, Item, Photos


@app.route("/")
def home():
    posts = [Posts(author_id=1, title="This is a title", body="This is a test post", responses="👍 👎 "),
             Posts(author_id=1, title="this is a title", body="This is a test post",
                   responses="This is a test post's meta data"),
             Posts(author_id=1, title="this is a title", body="This is a test post",
                   responses="This is a test post's meta data")]
    allCommunities = Communities.query.all()
    usersCommunities = []
    numberOfCommunities = 0
    if current_user.is_authenticated:
        for community in allCommunities:
            userlist = community.getUsers()
            numberOfCommunities = len(userlist)
            if current_user.username in userlist:
                usersCommunities.append(community)

                allCommunities.remove(community)

    # print(usersCommunities)
    # print(allCommunities)
    return render_template('home.html', usersCommunities=usersCommunities, allCommunities=allCommunities, posts=posts,
                           numberOfCommunities=numberOfCommunities)


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
    for i in Communities.query.all():
        if community_name == i.name:
            community = i
    if request.method == 'POST':
        if request.form['join'] == 'Join Community':
            community.addUser(current_user)
        elif request.form['join'] == 'Leave Community':
            community.removeUser(current_user)
    temp = community.collections[0]
    # print(temp)
    return render_template('community.html', community=community, user=current_user, temp=temp)


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
        # print(text2, community2)
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


@app.route("/collections/createCollection/<community_id>", methods=['GET', 'POST'])
def createCollection(community_id):
    form = createCollectionForm()

    if form.validate_on_submit():
        collection = Collections(form.name.data, form.desc.data, current_user.id, community_id)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("createCollection.html", title='Add Item', form=form)


@app.route("/fillDB")
def filldb():
    db.drop_all()
    db.create_all()
    db.session.add(User("Admin", "admin@kollekt.com", "testing"))
    db.session.add(Communities("Watches", "Timepieces"))
    db.session.add(Communities("Shoes", "Gloves for your feet"))
    db.session.add(Collections("Admins Shoes", "A collection of all of admins shoes", 1, 2))
    db.session.add(Item("Moses 300", "A pair of vegan leather Moses 300s", 1))
    db.session.add(Item("Better Call Saul 750", "My lawyers shoes", 1))
    db.session.commit()
    login_user(User.query.filter_by(id=1).first())
    allCommunities = Communities.query.all()
    # print(allCommunities)
    return redirect(url_for('home'))
