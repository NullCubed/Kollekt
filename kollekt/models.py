from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    desc = db.Column(db.String)
    users = db.Column(db.String)
    collections = db.relationship('Collections', backref='communities', lazy=True)

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.users = ""

    def getCollections(self):
        """
        Returns the [TBD] most recent collections in the community
        :return: list of references to [TBD] latest collections
        """
        return self.collections

    def getPosts(self):
        """
        Returns the [TBD] most recent posts in the community
        :return: list of references to [TBD] latest posts
        """
        return self.posts

    def addCollection(self, collection):
        """
        Adds a collection to the community
        :return: none
        """
        if collection not in self.collections:
            self.posts.append(collection)

    def removeCollection(self, collection):
        """
        Removes a collection from the community
        :return: none
        """
        if collection in self.collections:
            self.posts.remove(collection)

    def addPost(self, post):
        """
        Adds a post to the community
        :return: none
        """
        if post not in self.posts:
            self.posts.append(post)

    def removePost(self, post):
        """
        Removes a post from the community
        :return: none
        """
        if post in self.posts:
            self.posts.remove(post)

    def getUsers(self):
        """
        Returns a list of users in the community
        :return: list of users
        """
        userlist = self.users.split(";")
        return userlist

    def userHasJoined(self, user):
        """
        Returns a boolean if the user joined the given community
        :param user: a user to locate in the list of the community's followers
        :return: boolean (True if user joined community, else false)
        """
        try:
            if str(user.id) in self.getUsers():
                return True
            else:
                return False
        except AttributeError:
            return False

    def addUser(self, user):
        """
        Adds a user to the community
        :param user: a user to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(user):
            pass
        else:
            temp_user_list = self.getUsers()
            temp_user_list.append(str(user.id))
            self.users = ';'.join(temp_user_list)
            sa.update(db).values({"users": self.users}).where(db.c.users == "users")
            db.session.commit()

    def removeUser(self, user):
        """
        Removes a user from the community
        :param user: a user to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(user):
            temp_user_list = self.getUsers()
            temp_user_list.remove(str(user.id))
            self.users = ";".join(temp_user_list)
            sa.update(db).values({"users": self.users}).where(db.c.users == "users")
            db.session.commit()
        else:
            pass

    def getName(self):
        """
        Getter for the name of the community
        :return: name of community
        """
        return self.name

    def setName(self, name):
        """
        Setter for the name of the community
        :return: none
        """
        self.name = name

    def getDesc(self):
        """
        Getter for the description of the community
        :return: description of community
        """
        return self.desc

    def setDesc(self, desc):
        """
        Setter for the description of the community
        :return: none
        """
        self.desc = desc


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String)
    meta = db.Column(db.String)
    responses = db.Column(db.BLOB)
    item = db.Column(db.String)
