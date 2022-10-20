class User:
    """
    Created after a user logs in or signs up
    Uses the users user ID to talk with the database
    Parameters: user_id, name, isAdmin

    """

    def __init__(self, user_id: int, email: str, isAdmin: bool):
        self.user_id = user_id
        self.email = email
        self.isAdmin = isAdmin

    def getProfileInfo(self):
        return 'sample info'

    def getId(self):
        return self.user_id

    def getPosts(self):
        return 'post info'

    def addPost(self):
        return 'post added'

    def addInfo(self):
        return 'info added'
