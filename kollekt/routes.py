from .models import User, Communities, Collections, Posts, db
from flask_login import login_user, current_user, logout_user, login_required
from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from kollekt.forms import RegistrationForm, LoginForm, UserForm, ItemAddForm, createCommunityForm, deleteCommunityForm,createPostForm
# from .Components.Community import Community
# from .Components.Collection import CollectionItem


@app.route("/")
def home():
    posts = Posts.query.all()
    usersCommunities = []
    allCommunities = Communities.query.all()
    tempCommunities = allCommunities
    tempUsers = []
    if current_user.is_authenticated:
        print(allCommunities)
        for community in allCommunities:
            tempUsers = []
            for i in community.getUsers():
                tempUsers.append(i.username)
            print(tempUsers)
            if current_user.username in tempUsers:
                usersCommunities.append(community)
    tempComnames = []
    tempUserComNames = []
    for i in tempCommunities:
        tempComnames.append(i.name)
    for x in usersCommunities:
        tempUserComNames.append(x.name)
    for i in tempComnames:
        if i in tempUserComNames:
            tempCommunities.remove(Communities.query.filter_by(name=i).first())
    sampleCollections = Collections.query.all()
    sampleCommunities = Communities.query.all()
    collectionsCount = len(sampleCollections)
    communitiesCount = len(sampleCommunities)
    postCount = len(posts)
    usersCount = len(User.query.all())
    return render_template('home.html', postCount=postCount, collectionsCount=collectionsCount, communitiesCount=communitiesCount, usersCount=usersCount, sampleCommunities=sampleCommunities, sampleCollections=sampleCollections,
                           usersCommunities=usersCommunities, allCommunities=tempCommunities, posts=posts)


@app.route("/userProfile")
def userProfile():
    users_posts = []
    all_posts = Posts.query.all()
    print(all_posts)
    all_posts.reverse()
    print(all_posts)
    for i in all_posts:
        if i.author_id == current_user.id:
            users_posts.append(i)
    print(users_posts)
    posts = Posts.query.all()
    allCommunities = Communities.query.all()
    usersCommunities = []
    if current_user.is_authenticated:
        for community in allCommunities:
            print(community)
            userlist = community.getUsers()  # waiting for method implementation
            finalUserList = []
            for i in userlist:
                finalUserList.append(i.username)
            # userlist = []  # using this for now
            if current_user.username in finalUserList:
                usersCommunities.append(community)
                allCommunities.remove(community)
    sampleCollections = Collections.query.all()
    sampleCommunities = Communities.query.all()
    return render_template('test.html', sampleCommunities=sampleCommunities, sampleCollections=sampleCollections,
                           usersCommunities=usersCommunities, allCommunities=allCommunities, posts=posts, user=current_user, users_posts=users_posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/userSettings", methods=['GET', 'POST'])
@login_required
def userSettings():
    form = UserForm()
    id = current_user.id
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.bio = request.form['bio']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("settings.html",
                                   form=form,
                                   name_to_update=name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return render_template("settings.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
    else:
        return render_template("settings.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


@app.route("/userCard/<id>")
@login_required
def userCard(id):
    userInfo = User.query.filter_by(id=id).first()
    return render_template('userCard.html', userInfo=userInfo)


@app.route("/community/<url>", methods=['GET', 'POST'])
def communityPage(url):
    community = Communities.query.filter_by(url=url).first()
    posts_to_display = []
    print(posts_to_display)
    all_posts = Posts.query.all()
    print(all_posts)
    all_posts.reverse()
    print(all_posts)
    k = 0
    for j in all_posts:
        k += 1
        if j.community_id == community.id:
            posts_to_display.append(j)
        if k == 5:
            break
    print(posts_to_display)
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form['join'] == 'Join Community':
                community.addUser(current_user)
            elif request.form['join'] == 'Leave Community':
                community.removeUser(current_user)
        else:
            return redirect(url_for('login'))
    return render_template('community.html', community=community, user=current_user, posts_to_display=posts_to_display)


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
            flash(f'Login successful {user.username}', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong Password", "danger")
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
            flash("Username already taken", "danger")
            return redirect(url_for('register'))
        elif email:
            flash("Email already used", "danger")
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash(f'Registered {user.username}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/addItem", methods=['GET', 'POST'])
def addNewCollectionItem():
    form = ItemAddForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
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
            flash("Community already exists", "danger")
            return redirect(url_for('adminpage'))
        else:
            community = Communities(name=form.name.data,
                                    desc=form.description.data)
            db.session.add(community)
            db.session.commit()
        flash(f"Community Created: {community.name}", "success")
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
            flash("Community does not exist", "danger")
            return redirect(url_for('adminpage'))
    return render_template('adminpage.html', form=form, delform=delform, allCommunities=allCommunities)


@app.route("/community/<community_url>/<post_id>", methods=['GET', 'POST'])
def viewPost(community_url, post_id):
    post_to_view = Posts.query.filter_by(id=post_id).first()
    if post_to_view is None:
        return render_template('viewpost.html', post_to_view=post_to_view, community=None)
    community = Communities.query.filter_by(url=community_url).first()
    if post_to_view.getCommunity() is not community:  # if correct id but wrong community, corrects url
        return redirect(url_for('viewPost', community_url=post_to_view.getCommunity().url, post_id=post_id))
    return render_template('viewpost.html', post_to_view=post_to_view, community=community)


@app.route("/create_post", methods=['GET', 'POST'])
def addNewPost():
    if current_user.is_authenticated:
        form = createPostForm()
        can_post = False
        for i in Communities.query.all():  # check that user is part of at least 1 community
            if i.userHasJoined(current_user):
                can_post = True
                break
        if form.validate_on_submit():
            if form.body.data == "" and form.item_id.data == "":
                flash("Must enter text into the body or attach an item!", "Danger")
                return redirect(url_for('create_post'))
            else:
                target_community = Communities.query.filter_by(
                    name=form.community.data).first()
                new_post = Posts(author_id=current_user.id, title=form.title.data, body=form.body.data,
                                 community_id=target_community.id)
                print("new_post created")
                db.session.add(new_post)
                db.session.commit()
                print(new_post)
                print("committed to database")
                return redirect(url_for('viewPost', community_url=form.community.data, post_id=new_post.id))
        return render_template("createpost.html", form=form, can_post=can_post)
    else:
        return redirect(url_for('login'))
