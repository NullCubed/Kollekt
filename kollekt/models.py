from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


import sqlalchemy as sa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_in_community = db.Table('users_in_community',
                              db.Column('community_id', db.Integer,
                                        db.ForeignKey('communities.id')),
                              db.Column('user_id', db.Integer,
                                        db.ForeignKey('user.id'))
                              )
likes_on_posts = db.Table('likes_on_posts',
                          db.Column('post_id', db.Integer,
                                    db.ForeignKey('posts.id')),
                          db.Column('user_id', db.Integer,
                                    db.ForeignKey('user.id'))
                          )
dislikes_on_posts = db.Table('dislikes_on_posts',
                             db.Column('post_id', db.Integer,
                                       db.ForeignKey('posts.id')),
                             db.Column('user_id', db.Integer,
                                       db.ForeignKey('user.id'))
                             )


# TODO: Move all class files into this file and setup models to initialize DB tables etc.
#   Currently having issues with import loop ie importing db from index and then importing User from models
#   Restructuring should resolve this issue
#   Need help from Dr. Layman regarding the best way to go about this (?)


class User(db.Model, UserMixin):
    # id = db.Column(db.Integer, unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # communities = db.Column(db.BLOB)
    # collections = db.Column(db.BLOB)
    admin = db.Column(db.Boolean)
    profile_picture = db.Column(db.BLOB)
    bio = db.Column(db.VARCHAR)
    posts = db.relationship('Posts', backref='author', lazy=True)
    collections = db.relationship(
        'Collections', backref='collectionAuthor', lazy=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def getUserInfo(self):
        user = db.get_or_404(User, self.id)
        return user

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.password}>'


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collections.id'), nullable=False)


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    owner = db.Column(db.Integer)
    items = db.relationship('Items', backref='collections', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(
        db.Integer, db.ForeignKey('communities.id'), nullable=False)


class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    desc = db.Column(db.String)
    collections = db.relationship(
        'Collections', backref='communities', lazy=True)
    users = db.relationship(
        'User', secondary=users_in_community, backref='users')

    def __init__(self, name, desc):
        self.name = name
        self.url = name.lower().translate({ord(i): None for i in "'.,;:"}).replace('"', "").translate(
            {ord(i): "_" for i in " -"})
        self.desc = desc
        self.posts = []
        self.collections = []
        self.users = []

    def getCollections(self):
        """
        Returns a list of collections in the community
        :return: list of references to collections in the community
        """
        return self.collections

    def addCollection(self, collection):
        """
        Adds a collection to the community
        :return: none
        """
        if collection not in self.collections:
            self.collections.append(collection)
            db.session.commit()

    def removeCollection(self, collection):
        """
        Removes a collection from the community
        :return: none
        """
        if collection in self.collections:
            self.collections.remove(collection)
            db.session.commit()

    def getPosts(self):
        """
        Returns all posts in the community
        :return: list of references to posts in the community
        """
        return self.posts

    def addPost(self, post):
        """
        Adds a post to the community
        :return: none
        """
        if post not in self.posts:
            self.posts.append(post)
            db.session.commit()

    def removePost(self, post):
        """
        Removes a post from the community
        :return: none
        """
        if post in self.posts:
            self.posts.remove(post)
            db.session.commit()

    def userHasJoined(self, user_id):
        """
        Returns a boolean if the user joined the given community
        :param user_id: a user to locate in the list of the community's followers
        :return: boolean (True if user joined community, else false)
        """
        if user_id in self.users:
            return True
        return False

    def addUser(self, user_id):
        """
        Adds a user to the community
        :param user_id: a user id to locate in the list of the community's followers
        :return: none
        """
        if not self.userHasJoined(user_id):
            self.users.append(user_id)
            db.session.commit()

    def removeUser(self, user_id):
        """
        Removes a user from the community
        :param user_id: a user id to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(user_id):
            self.users.remove(user_id)
            db.session.commit()

    def getUsers(self):
        return self.users

    def memberCount(self):
        return len(self.users)

    def setName(self, name):
        """
        Setter for the name of the community. Also adjusts the url-name
        :return: none
        """
        self.name = name
        self.url = name.lower().translate({ord(i): None for i in "'.,;:"}).replace('"', "").translate(
            {ord(i): "_" for i in " -"})
        db.session.commit()

    def __repr__(self):
        return f'<Community "{self.url}">'


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String)
    timestamp = db.Column(db.String)
    meta = db.Column(db.String)
    comments = db.Column(db.BLOB)
    item_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)
    likes = db.relationship(
        'User', secondary=likes_on_posts, backref='usersWhoLiked')
    dislikes = db.relationship(
        'User', secondary=dislikes_on_posts, backref='usersWhoDisliked')

    def __init__(self, author_id, title, body, community_id, item_id=None):
        self.author_id = author_id
        self.title = title
        self.body = body
        self.community_id = community_id
        self.timestamp = str(datetime.datetime.now())
        self.likes = []
        self.dislikes = []
        self.item_id = item_id

    def getAuthor(self):
        return User.query.filter_by(id=self.author_id).first()

    def getCommunity(self):
        return Communities.query.filter_by(id=self.community_id).first()

    def getLinkedItem(self):
        return Items.query.filter_by(id=self.item_id).first()

    def getLikes(self):
        return len(self.likes)

    def getDislikes(self):
        return len(self.dislikes)

    def userHasLiked(self, user_id):
        if user_id in self.likes:
            return True
        return False

    def userHasDisliked(self, user_id):
        if user_id in self.dislikes:
            return True
        return False

    def toggleLike(self, user_id):
        if user_id in self.likes:
            self.likes.remove(user_id)
        else:
            if user_id in self.dislikes:
                self.dislikes.remove(user_id)
            self.likes.append(user_id)
        db.session.commit()

    def toggleDislike(self, user_id):
        if user_id in self.dislikes:
            self.dislikes.remove(user_id)
        else:
            if user_id in self.likes:
                self.likes.remove(user_id)
            self.dislikes.append(user_id)
        db.session.commit()

    def getTimestamp(self):
        # returns post time if posted today, otherwise returns post date
        now = str(datetime.datetime.now()).split(" ")
        post_time_for_eval = self.timestamp.split(" ")
        if now[0] == post_time_for_eval[0]:
            # second return val used specifically for formatting on post display
            return post_time_for_eval[1].split(".")[0], "at " + post_time_for_eval[1].split(".")[0]
        else:
            return post_time_for_eval[0], "on " + post_time_for_eval[0]

    def __repr__(self):
        return f'<Post #{self.id} in Community "{self.getCommunity().url}">'


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.String)
    timestamp = db.Column(db.String)
    meta = db.Column(db.String)
    locked = db.Column(db.Boolean)

    def __init__(self, author_id, text, post_id):
        self.author_id = author_id
        self.post_id = post_id
        self.text = text
        self.timestamp = str(datetime.datetime.now())
        self.locked = False

    def getAuthor(self):
        return User.query.filter_by(id=self.author_id).first()

    def getPost(self):
        return Posts.query.filter_by(id=self.post_id).first()

    def isLocked(self):
        return self.locked

    def setText(self, text):
        self.text = text
        db.session.commit()

    def lockPost(self):
        self.text = "This comment has been removed by an administrator."
        self.locked = True
        db.session.commit()

    def getTimestamp(self):
        # returns post time if posted today, otherwise returns post date
        now = str(datetime.datetime.now()).split(" ")
        post_time_for_eval = self.timestamp.split(" ")
        if now[0] == post_time_for_eval[0]:
            # second return val used specifically for formatting on post display
            return post_time_for_eval[1].split(".")[0], "at " + post_time_for_eval[1].split(".")[0]
        else:
            return post_time_for_eval[0], "on " + post_time_for_eval[0]

    def __repr__(self):
        return f'<comment #{self.id} under post #{self.post_id} in community "{self.getCommunity().url}">'
