import os

from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_in_community = db.Table('users_in_community',
                              db.Column('community_id', db.Integer,
                                        db.ForeignKey('communities.id')),
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

    def __init__(self, username, email, password):
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


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collections.id'), nullable=False)
    picture = db.Column(db.BLOB)
    picture_path = db.Column(db.String)

    def convertToBinaryData(self, filepath):
        # Convert digital data to binary format
        with open(filepath, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def write_file(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)

    def __init__(self, name, desc, collection_id):
        self.name = name
        self.desc = desc
        self.collection_id = collection_id
        self.picture_path = 'kollekt/static/bantest.png'
        self.picture = self.convertToBinaryData(self.picture_path)


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    # owner = db.Column(db.Integer)
    items = db.relationship('Item', backref='collections', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(
        db.Integer, db.ForeignKey('communities.id'), nullable=False)

    def __init__(self, name, desc, user_id, community_id):
        self.name = name
        self.desc = desc
        self.user_id = user_id
        self.community_id = community_id

    def __repr__(self):
        return f'<Collection {self.name}, {self.items}, {self.community_id}>'

    def getItem(self):
        item = self.items[0]
        item.write_file(item.picture, item.picture_path)
        return f'<img src=\"../static/bantest.png\" width=100 height=100/>' \
               f'<br />' \
               f'<h4 class=\"text-center\">{item.name}<br/>{item.desc}</h4>'


class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collections = db.relationship(
        'Collections', backref='communities', lazy=True)

    def getUsers(self):
        return [x for x in range(100)]

    users_in_communities = db.relationship(
        'User', secondary=users_in_community, backref='users')

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String)
    meta = db.Column(db.String)
    responses = db.Column(db.BLOB)
    item = db.Column(db.String)
