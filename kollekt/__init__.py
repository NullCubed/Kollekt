from time import sleep
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cdesntysuitrba' \
    #                                         ':42ed85406d44789ac58a6b6b178f6804cb4081db461a5659cfd12c20ec172b22@ec2-52' \
    #                                         '-200-5-135.compute-1.amazonaws.com:5432/d2inpdhdbc01g6'



    db.init_app(app)

    with app.app_context():
        from . import routes
        if os.path.isfile('instance\site.db'):
            os.remove('instance\site.db')
            print("Deleted local db")
            sleep(10)
        db.create_all()
        print("Initialized tables in local db")
        print("** Filled tables in db with dummy info")
        return app
