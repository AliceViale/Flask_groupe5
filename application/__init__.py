from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'didyouknow.db'

def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['ENV']='developement'
    app.config['SCRET_KEY'] = 'allhailsatan'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .models import Knowledge
    create_database(app)
    from .views import views
    app.register_blueprint(views,url_prefix='/')
    return app

def create_database(app):
    if not path.exists("application/"+DB_NAME):
        db.create_all(app=app)
        print('Created Database!')