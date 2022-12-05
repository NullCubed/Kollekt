# CSC 450 - Team Project

## Team Members

# Parker Gagliano

# William Pridgen

# Garrett McGhee

# Trent Salas

# Josh Mertz

## Instructions to build/run/test

Step 0: Install the following: [Python](https://realpython.com/installing-python/), an IDE [VS Code](https://code.visualstudio.com/docs/introvideos/basics) (Be sure you install the python extension!), [PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html#silent)

Step 1: Pull the most recent version of the repo to your local machine using git cli or GitHub desktop app

Step 2: Open the project in your IDE of choice

Step 3: If developing open .env and ensure ```CONFIG_TYPE = config.DevelopmentConfig```

Step 4: run ```pip install -r requirements.txt``` in terminal

Step 5: Run /kollekt/run.py

Also you can enter in your terminal ```flask shell``` while the app is running and you can now pass commands etc. to the app for example: ```db.drop_all(), db.create_all(), User.query.all()```

Step 6: Click/copy link in output to see website deployed on local Flask server

## Testing Instructions

You can either run ```python -m pytest testing.py``` or your IDE might suggest running testing using testing.py and it makes working with the tests easier (auto-run etc.)

For coverage test you can run with coverage (in PyCharm confirmed) by clicking 'run with coverage'

