from kollekt.User import User


class Community:

    def __init__(self, community_name):
        # self._template = template
        self._name = community_name
        self._posts = []
        self._collections = []
        self._users = []

    def getCollections(self):
        """
        Returns the [TBD] most recent collections in the community
        :return: list of references to [TBD] latest collections
        """
        return self._collections

    def getPosts(self):
        """
        Returns the [TBD] most recent posts in the community
        :return: list of references to [TBD] latest posts
        """
        return self._posts

    def addCollection(self, _collection):
        """
        Adds a collection to the community
        :return: none
        """
        if _collection not in self._collections:
            self.posts.append(_collection)

    def removeCollection(self, _collection):
        """
        Removes a collection from the community
        :return: none
        """
        if _collection in self._collections:
            self.posts.remove(_collection)

    def addPost(self, _post):
        """
        Adds a post to the community
        :return: none
        """
        if _post not in self.posts:
            self.posts.append(_post)

    def removePost(self, _post):
        """
        Removes a post from the community
        :return: none
        """
        if _post in self.posts:
            self._posts.remove(_post)

    def userHasJoined(self, _user):
        """
        Returns a boolean if the user joined the given community
        :param _user: a user to locate in the list of the community's followers
        :return: boolean (True if user joined community, else false)
        """
        if _user in self._users:
            return True
        else:
            return False

    def getUsers(self):
        """
        Returns a list of users in the community
        :return: list of users
        """
        return self._users

    def addUser(self, _user):
        """
        Adds a user to the community
        :param _user: a user to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(_user):
            pass
        else:
            self._users.append(_user)

    def removeUser(self, _user):
        """
        Removes a user from the community
        :param _user: a user to locate in the list of the community's followers
        :return: none
        """
        if self.userHasJoined(_user):
            self.users.remove(_user)
        else:
            pass

    def toggleFollow(self, _user):
        """
        Invokes add_user or remove_user depending on whether the user is in the community
        :param _user: a user to locate in the list of the community's followers
        :return: nothing
        """
        if self.userHasJoined(_user):
            self.addUser(_user)
        else:
            self.removeUser(_user)

    def getName(self):
        """
        Getter for the name of the community
        :return: name of community
        """
        return self._name

    def setName(self, _name):
        """
        Getter for the name of the community
        :return: name of community
        """
        self._name = _name

    posts = property(getPosts, addPost)
    users = property(getUsers)
    collections = property(getCollections, addCollection)
    name = property(getName, setName)
