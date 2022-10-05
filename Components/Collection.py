class collection:
    def __int__(self,user,community,items,template):
        self.user = user
        self.community = community
        self.items = []
        self.template = template

    def add_collection_item(self,photo,text):
        """
        This method adds a collection item to the item list of the collection. It will raise an exception if the photo or text
        is in the incorrect format.
        :param photo: A photo that will be attached to represent the collection item
        :param text: text that represent the item
        :return: position in collection list
        """
    def add_reaction(self,user,reaction,item):
        """
        This method adds a reaction to the collection item
        :param user: the user that is adding the reaction
        :param reaction: the reaction that is being added
        :param item: the item that the reaction is being added to
        :return: nothing
        """
    def item_info(self, item):
        """
        this method returns a list of info about the item
        :param item: the item that information is requested for
        :return: a list of item info
        """







