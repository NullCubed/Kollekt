

class Collection:

    def __init__(self, community, template, user):
        self._template = template
        self._user = user
        self._community = community
        self.items = []

    def add_collection_item(self, collection_item):
        """
        This method adds a collection item to the item list of the collection.
        param collection_item: The collection item object to is to be added to the list of items
        :return: position in collection list
        """

        self.items.append(collection_item)
        return len(self.items)

    def get_collection_item(self, index):
        """
        used to return the collection item in the given index in the list of items
        :param index: the index position to return from the list of collection items
        :return:the collection item at items[index]
        """
        return self.items[index]

    def get_user(self):
        """
        Returns the user that owns the collection
        :return: the user that owns the collection
        """
        return self._user

    def get_community(self):
        """
        Returns the community that the collection is a part of
        :return: assigned community
        """
        return self._community

    def get_items(self):
        """
        Returns the whole list of items in the collection
        :return: the list of items
        """
        return self.items

    def get_template(self):
        """
        Returns the template that the collection uses for it collection items
        :return: the template of the collection
        """
        return self._template

    def set_user(self, user):
        """
        sets the user that owns the collection
        :param user: the user that the collection's user will be set to
        :return: nothing
        """
        self._user = user

    def set_community(self, community):
        """
        sets the community that the collection is a part of
        :param community: the community that the collection will be assigned to
        :return: nothing
        """
        self._community = community

    def set_template(self, template):
        """
        sets the template that the collection uses for the collection items
        :param template: the template to be assigned
        :return: nothing
        """
        self._template = template

    user = property(get_user, set_user)
    community = property(get_community, set_community)
    template = property(get_template, set_template)


# class Reaction:
#     def __init__(self,user,item):


class CollectionItem:

    def __init__(self, user, community, template, photo, text, collection,likes,dislikes,likers,dislikeers):
        self._collection = collection
        self._user = user
        self._community = community
        self._template = template
        self._photo = photo
        self._text = text
        self.reactions = []
        self.likes = 0
        self.disliskes = 0
        self.likers = []
        self.dislikers = []




    def get_user(self):
        """
        returns the user that owns the collection item
        :return: the user of the collection item
        """
        return self._user

    def get_community(self):
        """
        returns the community that the collection item is a part of
        :return:the set community
        """
        return self._community

    def get_template(self):
        """
        returns the template that the collection item is using
        :return: current set template
        """
        return self._template

    def get_photo(self):
        """
        returns the photo that the collection item has assigned
        :return: current photo
        """
        return self._photo

    def get_text(self):
        """
        returns the text for the collection item description
        :return: current set text
        """
        return self._text

    def get_collection(self):
        """
        returns the collection of the item
        :return: the item's set collection
        """
        return self._collection

    def set_user(self, user):
        """
        sets the user of the collection item
        :param user: the user that is to be set for the collection item
        :return: nothing
        """
        self._user = user

    def set_community(self, community):
        """
        sets the community that the collection item is assigned to
        :param community: the community that the item is to be set to
        :return: nothing
        """
        self._community = community

    def set_template(self, template):
        """
        Sets the template that the item will use
        :param template: the template to be set
        :return: nothing
        """
        self._template = template

    def set_photo(self, photo):
        """
        sets the photo for the collection item
        :param photo: the photo that is to be used for the collection item
        :return: nothing
        """
        self._photo = photo

    def set_text(self, text):
        """
        sets the text for the collection item
        :param text: the text that is to be set for the collection item
        :return: nothing
        """
        self._text = text

    def set_collection(self, collection):
        """
        sets the collection that the item is a part of
        :param collection: the collection that the item is added to
        :return: nothing
        """
        collection.add_collection_item(self)
        self._collection = collection

    # def item_info(self, item):
    #     """
    #     this method returns a list of info about the item
    #     :param item: the item that information is requested for
    #     :return: a list of item info
    #     """

    def add_reaction(self, reaction):
        """
        This method adds a reaction to the collection item
        :param reaction: the reaction that is being added
        :return: nothing
        """
        self.reactions.append(reaction)

    def get_reaction(self):
        """
        returns the list of reactions for the item
        :return: list of reactions
        """
        return self.reactions
    def add_like(self):
        self.likes += 1
        return(self.likes)
    def add_dislike(self):
        self.disliskes += 1
        return (self.disliskes)
    def add_like(self,user_who_liked):
        if user_who_liked not in self.likers():
            self.likers.append(user_who_liked)
            self.likes += 1
            return self.likes
        else:
            self.likers.remove(user_who_liked)
            self.likes -= 1
            return self.likes
    def add_dislike(self,user_who_disliked):
        if user_who_disliked not in self.dislikers():
            self.dislikers.append(user_who_disliked)
            self.dislikes += 1
            return self.dislikes
        else:
            self.dislikers.remove(user_who_disliked)
            self.dislikes -= 1
            return self.dislikes


    photo = property(get_photo, set_photo)
    user = property(get_user, set_user)
    community = property(get_community, set_community)
    template = property(get_template, set_template)
    reaction = property(get_reaction, add_reaction)


