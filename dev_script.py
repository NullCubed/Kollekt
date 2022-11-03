import datetime
import os


def delete_db():
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if name == "site.db":
                os.remove(os.path.join(root, name))
                print("Database Deleted")


def fill_db():
    exit()
