class Collection:
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
class CollectionItem:
    def __init__  (self)
        self._user = None
        self._community = None
        self._template = None
    def get_user(self):
        return self._user
    def get_community(self):
        return self._community
    def get_template(self):
        return self._template
    def set_user(self,user):
        self._user = user
    def set_community(self,community):
        self._community = community
    def set_template(self,template):
        self._template = template
    user = property(get_user,set_user)
    community = property(get_community,set_community)
    template = property(get_template,set_template)







