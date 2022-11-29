import os

from .models import User, Communities, Collections, Posts, db, CollectionItem, Comments
from flask_login import login_user, current_user, logout_user, login_required
from flask import current_app as app
from flask import render_template, url_for, flash, redirect, request
from werkzeug.utils import secure_filename
from kollekt.forms import RegistrationForm, LoginForm, UserForm, ItemAddForm, createCommunityForm, \
    deleteCommunityForm, createPostForm, createCommentForm, editPostForm, deletePostForm, createCollectionForm


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

        for community in allCommunities:
            tempUsers = []
            for i in community.getUsers():
                tempUsers.append(i.username)
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
    return render_template('home.html', postCount=postCount, collectionsCount=collectionsCount,
                           communitiesCount=communitiesCount, usersCount=usersCount,
                           sampleCommunities=sampleCommunities, sampleCollections=sampleCollections,
                           usersCommunities=usersCommunities, allCommunities=tempCommunities, posts=posts)


@app.route("/userProfile")
def userProfile():
    users_posts = []
    all_posts = Posts.query.all()
    all_posts.reverse()
    for i in all_posts:
        if i.author_id == current_user.id:
            users_posts.append(i)
    posts = Posts.query.all()
    allCommunities = Communities.query.all()
    usersCommunities = []
    if current_user.is_authenticated:
        collection_user = current_user.collections
        for community in allCommunities:
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
                           usersCommunities=usersCommunities, allCommunities=allCommunities, posts=posts,
                           user=current_user, users_posts=users_posts, users_collections=collection_user)


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
    all_posts = Posts.query.all()
    all_posts.reverse()
    k = 0
    for j in all_posts:
        k += 1
        if j.community_id == community.id:
            posts_to_display.append(j)
        if k == 5:
            break
    if request.method == 'POST':
        if current_user.is_authenticated:
            if request.form['join'] == 'Join Community':
                community.addUser(current_user)
            elif request.form['join'] == 'Leave Community':
                community.removeUser(current_user)
                for i in Collections.query.filter_by(user_id=current_user.id):
                    if i.community_id == community.id:
                        db.session.delete(i)
                        db.session.commit()

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
            user = User(username, email, password, False)
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


@app.route("/addItem/<collection_id>", methods=['GET', 'POST'])
def addNewCollectionItem(collection_id):
    if current_user.is_authenticated:
        form = ItemAddForm()
        print('added12', Collections.query.filter_by(id=collection_id).first())
        add_community = Collections.query.filter_by(id=collection_id).first().community_id
        print('add_community:', add_community)
        add_collection = Collections.query.filter_by(id=collection_id).first().id
        print("add_collection:", add_collection)

        if form.validate_on_submit():
            filename = secure_filename(form.photo.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path = file_path.replace("\\", "/")
            form.photo.data.save(file_path)
            print('user:',current_user.id)
            collection_item = CollectionItem(user=current_user.id,community=add_community,photo=filename,
                                             desc=form.text.data, collection=add_collection,name=form.name.data)

            print("item",collection_item)

            db.session.add(collection_item)
            db.session.commit()
            return render_template("item.html", title="Your Item", item=collection_item, filename=filename)
        print(form.errors)
        return render_template("addItem.html", title='Add Item', form=form)
    else:
        return redirect(url_for('login'))


@app.route("/adminpage", methods=['GET', 'POST'])
def adminpage():
    print(current_user.admin)
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
            postsToDelte = checkCommunity.getPosts()
            for i in postsToDelte:
                db.session.delete(i)
            collectionsToDelete = checkCommunity.getCollections()
            for i in collectionsToDelete:
                db.session.delete(i)
            db.session.delete(checkCommunity)
            db.session.commit()
            flash(f"Community Deleted {checkCommunity.name}", "success")
            return redirect(url_for('adminpage'))
        else:
            flash("Community does not exist", "danger")
            return redirect(url_for('adminpage'))
    return render_template('adminpage.html', form=form, delform=delform, allCommunities=allCommunities)


@app.route("/collections/create/<community_id>", methods=['GET', 'POST'])
def createCollection(community_id):
    form = createCollectionForm()

    if form.validate_on_submit():
        collection = Collections(
            form.name.data, form.desc.data, current_user.id, community_id)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("createCollection.html", title='Add Item', form=form)


@app.route("/collections/view/<collection_id>", methods=['GET', 'POST'])
def viewCollection(collection_id):
    collection = Collections.query.filter_by(id=collection_id).first()
    return render_template("collections.html", collection=collection)


@app.route("/fillDB")
def filldb():
    db.drop_all()
    db.create_all()
    db.session.add(User("Admin", "admin@kollekt.com", "testing", True))
    db.session.add(Communities("Watches", "Timepieces"))
    db.session.add(Communities("Shoes", "Gloves for your feet"))
    db.session.add(Collections(
        "Admins Shoes", "A collection of all of admins shoes", 1, 2))
    db.session.add(Collections("Admins Watches",
                               "A collection of all of admins shoes", 1, 1))
    db.session.commit()
    login_user(User.query.filter_by(id=1).first())
    allCommunities = Communities.query.all()
    # print(allCommunities)
    return redirect(url_for('home'))


@app.route("/community/<community_url>/<post_id>", methods=['GET', 'POST'])
def viewPost(community_url, post_id):
    post_to_view = Posts.query.filter_by(id=post_id).first()
    if post_to_view is None:
        return render_template('viewpost.html', post_to_view=post_to_view, community=None)
    community = Communities.query.filter_by(url=community_url).first()
    if post_to_view.getCommunity() is not community:  # if correct id but wrong community, corrects url
        return redirect(url_for('viewPost', community_url=post_to_view.getCommunity().url, post_id=post_id))
    form = createCommentForm()
    if form.validate_on_submit():
        new_comment = Comments(author_id=current_user.id,
                               text=form.text.data, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
    comments = Comments.query.filter_by(post_id=post_id).all()
    # clears comment box upon posting; otherwise comment text remains in box
    form.text.data = ""
    return render_template('viewpost.html', post_to_view=post_to_view, community=community,
                           comments=comments, comment_count=len(comments), form=form)


@app.route("/community/<community_url>/create_post", methods=['GET', 'POST'])
def addNewPost(community_url):
    if current_user.is_authenticated:
        community = Communities.query.filter_by(url=community_url).first()
        if community.userHasJoined(current_user) is False:
            flash("Must be part of this community to make a post!", "danger")
            return redirect(url_for('communityPage', url=community_url))
        form = createPostForm()
        if form.validate_on_submit():
            if form.body.data == "":  # and form.item_id.data == "":
                flash("Must enter text into the body or attach an item!", "danger")
                return redirect(url_for('addNewPost', community_url=community_url))
            else:
                new_post = Posts(author_id=current_user.id, title=form.title.data, body=form.body.data,
                                 community_id=community.id)
                db.session.add(new_post)
                db.session.commit()
                flash(
                    f"Post {new_post.id} created in Community {community.url}", "success")
                return redirect(url_for('viewPost', community_url=community_url, post_id=new_post.id))
        return render_template("createpost.html", form=form)
    else:
        return redirect(url_for('login'))


@app.route("/community/<community_url>/<post_id>/edit", methods=['GET', 'POST'])
def editPost(community_url, post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('home'))
    if current_user.is_authenticated and post.getAuthor() == current_user:
        form = editPostForm()
        if form.validate_on_submit():
            if form.body.data == "":  # and form.item_id.data == "":
                flash("Must enter text into the body or attach an item!", "danger")
                return redirect(url_for('editPost', community_url=community_url, post_id=post_id))
            else:
                # post.setLinkedItem(form.item_id.data)
                post.setBody(form.body.data)
                db.session.commit()
                flash(
                    f"Post {post.id} in Community {community_url} edited", "success")
                return redirect(url_for('viewPost', community_url=community_url, post_id=post_id))
        form.body.data = post.body
        return render_template("editpost.html", form=form, community_url=community_url, post_id=post_id)
    else:
        return redirect(url_for('viewPost', community_url=community_url, post_id=post_id))


@app.route("/community/<community_url>/<post_id>/delete", methods=['GET', 'POST'])
def delPost(community_url, post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('home'))
    if current_user.is_authenticated and post.getAuthor() == current_user:
        form = deletePostForm()
        if form.validate_on_submit():
            if form.submitCancel.data:
                return redirect(url_for('viewPost', community_url=community_url, post_id=post_id))
            elif form.submitConfirm.data:
                post_title = post.title
                post.clearComments()
                db.session.delete(post)
                db.session.commit()
                flash("Post " + post_title + " has been deleted", "danger")
                return redirect(url_for('communityPage', url=community_url))
        return render_template("delpost.html", form=form, post=post)
    else:
        return redirect(url_for('viewPost', community_url=community_url, post_id=post_id))


@app.route("/comment/<comment_id>/delete", methods=['GET', 'POST'])
def delComment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    if comment is None:
        return redirect(url_for('home'))
    post = comment.getPost()
    community = post.getCommunity()
    if current_user.is_authenticated and comment.getAuthor() == current_user and comment.isLocked() is False:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted", "danger")
    # if current_user is admin, lock the post instead of deleting it
    return redirect(url_for('viewPost', community_url=community.url, post_id=post.id))
