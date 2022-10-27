import datetime
import os


def delete_db():
    if os.path.isfile("instance/site.db"):
        os.remove('instance/site.db')
        print("Deleted site.db at ", datetime.datetime.now().time())


def fill_db():
    exit()
