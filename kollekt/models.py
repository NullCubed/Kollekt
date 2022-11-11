from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
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
    communities = db.Column(db.BLOB)
    collections = db.Column(db.BLOB)
    admin = db.Column(db.Boolean)
    profile_picture = db.Column(db.BLOB)
    bio = db.Column(db.VARCHAR)
    posts = db.relationship('Posts', backref='author', lazy=True)
    collections = db.relationship(
        'Posts', backref='collectionAuthor', lazy=True)

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

    def userHasJoined(self, user):
        """
        Returns a boolean if the user joined the given community
        :param user: a user to locate in the list of the community's followers
        :return: boolean (True if user joined community, else false)
        """
        if user in self.users:
            return True
        return False

    def addUser(self, user):
        """
        Adds a user to the community
        :param user: a user to locate in the list of the community's followers
        :return: none
        """
        if not self.userHasJoined(user):
            self.users.append(user)
            db.session.commit()

    def removeUser(self, user):
        """
        Removes a user from the community
        :param user: a user to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(user):
            self.users.remove(user)
            db.session.commit()

    def setName(self, name):
        """
        Setter for the name of the community. Also adjusts the url-name
        :return: none
        """
        self.name = name
        self.url = name.lower().translate({ord(i): None for i in "'.,;:"}).replace('"', "").translate(
            {ord(i): "_" for i in " -"})
        db.session.commit()

    def memberCount(self):
        return len(self.users)

    def __repr__(self):
        return f'<Community "{self.url}">'


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # author = db.Column(db.String)
    title = db.Column(db.String)
    body = db.Column(db.String)
    # meta = db.Column(db.String)
    # responses = db.Column(db.BLOB)
    item_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)
    likes = db.relationship(
        'User', secondary=likes_on_posts, backref='usersWhoLiked')
    dislikes = db.relationship(
        'User', secondary=dislikes_on_posts, backref='usersWhoDisliked')

    def __init__(self, author, title, body, community, item=None):
        self.author_id = author.id
        # self.author = author
        self.title = title
        self.body = body
        self.community_id = community.id
        self.likes = []
        self.dislikes = []
        if item is not None:
            self.item_id = item.id

    def getAuthor(self):
        return User.query.filter_by(id=self.author_id).first()

    def getCommunity(self):
        return Communities.query.filter_by(id=self.community_id).first()

    def __repr__(self):
        return f'<Post #{self.id} in Community "{self.getCommunity().url}">'
