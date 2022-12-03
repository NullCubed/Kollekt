from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


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
    password = db.Column(db.String, nullable=False)
    # communities = db.Column(db.BLOB)
    # collections = db.Column(db.BLOB)
    admin = db.Column(db.Boolean)
    profile_picture = db.Column(db.String)
    bio = db.Column(db.VARCHAR)
    posts = db.relationship('Posts', backref='author', lazy=True)
    collections = db.relationship(
        'Collections', backref='collectionAuthor', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, email, password, admin):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.admin = admin

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
        
    def addCollection(self, collection):
        self.collections_list.append(collection)
        db.session.commit()

    def removeCollection(self, collection):
        if collection in self.collections_list:
            # print(self.collections_list)
            self.collections_list.remove(collection)
            # print(self.collections_list)
            db.session.commit()

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.password}, {self.collections}>'


class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    photo = db.Column(db.String)
    # likes = db.Column(db.Integer)
    # dislikes = db.Column(db.Integer)
    community_id = db.Column(db.Integer, db.ForeignKey(
        'communities.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey(
        'collections.id'), nullable=False)

    # picture = db.Column(db.BLOB)
    # filename = db.Column(db.String)

    # def convertToBinaryData(self, filepath):
    #     # Convert digital data to binary format
    #     with open(filepath, 'rb') as file:
    #         binaryData = file.read()
    #     return binaryData
    #
    # def write_file(self, data, filename):
    #     # Convert binary data to proper format and write it on Hard Disk
    #     with open(filename, 'wb') as file:
    #         file.write(data)

    def __init__(self, user, community, photo, desc, collection, name):
        self.collection_id = collection
        self.user = user
        self.community_id = community
        self.photo = photo
        self.desc = desc
        # self.likes = 0
        # self.dislikes = 0
        # self.likers = []
        # self.dislikers = []
        self.name = name

    # def add_like(self):
    #     self.likes += 1
    #     return self.likes
    #
    # def add_dislike(self):
    #     self.disliskes += 1
    #     return self.disliskes
    #
    # def add_liker(self, user_who_liked):
    #     if user_who_liked not in self.likers():
    #         self.likers.append(user_who_liked)
    #         self.likes += 1
    #         return self.likes
    #     else:
    #         self.likers.remove(user_who_liked)
    #         self.likes -= 1
    #         return self.likes
    #
    # def add_disliker(self, user_who_disliked):
    #     if user_who_disliked not in self.dislikers():
    #         self.dislikers.append(user_who_disliked)
    #         self.dislikes += 1
    #         return self.dislikes
    #     else:
    #         self.dislikers.remove(user_who_disliked)
    #         self.dislikes -= 1
    #         return self.dislikes
    def __repr__(self):
        return f'<CollectionItem {self.name}, {self.user}, {self.community_id}, {self.collection_id}>'


class Collections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    items = db.relationship(
        'CollectionItem', backref='Collections', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(
        db.Integer, db.ForeignKey('communities.id'), nullable=False)
    kind = db.Column(db.String)

    def __init__(self, name, desc, user_id, community_id):
        self.name = name
        self.desc = desc
        self.user_id = user_id
        self.community_id = community_id
        self.items = []
        self.kind = "collection"

    def __repr__(self):
        return f'<Collection {self.name}, {self.items}, {self.community_id}>'

    def getId(self):
        return self.user_id


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
        self.desc = desc
        self.url = name.lower().translate({ord(i): None for i in "'.,;:"}).replace('"', "").translate(
            {ord(i): "_" for i in " -"})
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
        posts = Posts.query.filter_by(community_id=self.id).all()
        print(posts)
        return posts

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
    photo_blob = db.Column(db.String)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String)
    timestamp = db.Column(db.String)
    meta = db.Column(db.String)
    comments = db.Column(db.String)
    item_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)
    likes = db.relationship(
        'User', secondary=likes_on_posts, backref='usersWhoLiked')
    dislikes = db.relationship(
        'User', secondary=dislikes_on_posts, backref='usersWhoDisliked')
    kind = db.Column(db.String)

    def __init__(self, author_id, title, body, community_id, item_id=None):
        self.author_id = author_id
        self.title = title
        self.body = body
        self.community_id = community_id
        self.timestamp = str(datetime.datetime.now())
        self.likes = []
        self.dislikes = []
        self.item_id = item_id
        self.kind = "post"

    def getAuthor(self):
        """
        Gets the author of the post.
        :return: User whose ID is stored in self.author_id
        """
        return User.query.filter_by(id=self.author_id).first()

    def getCommunity(self):
        """
        Gets the community which the post belongs to.
        :return: Community whose ID is stored in the post object
        """
        return Communities.query.filter_by(id=self.community_id).first()

    def setBody(self, body):
        """
        Sets the text of the body of the post.
        :param: body: the new text for the body.
        :return: none
        """
        self.body = body

    def getComments(self):
        """
        Gets all comments which are attached to the post.
        :return: List of comments
        """
        return Comments.query.filter_by(post_id=self.id).all()

    def clearComments(self):
        """
        Deletes all comments which are attached to the post; called prior to deleting the post.
        :return: None
        """
        comments = self.getComments()
        for i in comments:
            db.session.delete(i)
        db.session.commit()

    def getTimestamp(self):
        """
        Gets the raw timestamp and a formatted variant of it for display on the UI, depending on the current date.
        :return: Tuple of the raw timestamp and the formatted version
        """
        now = str(datetime.datetime.now()).split(" ")
        post_time_for_eval = self.timestamp.split(" ")
        if now[0] == post_time_for_eval[0]:
            return self.timestamp, "at " + post_time_for_eval[1].split(".")[0]
        else:
            return self.timestamp, "on " + post_time_for_eval[0]

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
        """
        Gets the author of the comment.
        :return: User whose ID is stored in self.author_id
        """
        return User.query.filter_by(id=self.author_id).first()

    def getPost(self):
        """
        Gets the post to which the comment belongs.
        :return: Post whose ID is stored in self.post_id
        """
        return Posts.query.filter_by(id=self.post_id).first()

    def isLocked(self):
        """
        Determines if the post has been locked by an administrator.
        :return: Boolean stored in self.locked.
        """
        return self.locked

    def setText(self, text):
        """
        Sets the text of the comment.
        :param: text: the new text for the comment.
        :return: none
        """
        self.text = text
        db.session.commit()

    def lockComment(self):
        """
        Locks the comment by setting self.locked to True and replacing the text. Used instead of deletion when a
        specific comment to a post is deleted by an administrator.
        :return: none
        """
        self.text = "This comment has been removed by an administrator."
        self.locked = True
        db.session.commit()

    def __repr__(self):
        return f'<comment #{self.id} under post #{self.post_id} in community "{self.getCommunity().url}">'
