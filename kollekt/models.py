from flask import Flask
from . import db, login_manager
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# HACK: Temp var until things can be rearranged


# TODO: Move all class files into this file and setup models to initialize DB tables etc.
#   Currently having issues with import loop ie importing db from index and then importing User from models
#   Restructuring should resolve this issue
#   Need help from Dr. Layman regarding the best way to go about this (?)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    communities = db.Column(db.BLOB)
    collections = db.Column(db.BLOB)
    admin = db.Column(db.Boolean())
    profile_picture = db.Column(db.BLOB)
    settings = db.Column(db.BLOB)

    def getUserInfo(self):
        user = db.get_or_404(User, self.id)
        return user

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    collectionID = db.Column(db.Integer)


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    communityID = db.Column(db.Integer)
    owner = db.Column(db.Integer)


class Communities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_blob = db.Column(db.BLOB)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    body = db.Column(db.String)
    meta = db.Column(db.String)
    responses = db.Column(db.BLOB)
    item = db.Column(db.String)
