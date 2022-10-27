class community:

    def __init__(self, template):
        self._template = template
        self.posts = []
        self.collections = []
        self.users = []

    def get_collections(self):
        """
        Returns the whole list of items in the collection
        :return: list of references to 10 latest posts
        """
        return self.collections

    def get_users(self):
        """
        Returns the whole list of items in the collection
        :return: list of users
        """
        return self.users

    def get_posts(self):
        """
        Returns the whole list of items in the collection
        :return: list of references to 10 latest posts
        """
        return self.posts

    def userHasJoined(self, user):
        """
        Returns a boolean if the user joined the given community
        :param user: a user to locate in the list of the community's followers
        :return: boolean (True if user joined community, else false)
        """
        if user in self.users:
            return True
        else:
            return False

    def toggleCommunity(self, user):
        """
        Returns a boolean if the user joined the given community
        :param user: a user to locate in the list of the community's followers
        :return: nothing
        """
        if self.userHasJoined(user):
            self.users.remove(user)
        else:
            self.users.append(user)

