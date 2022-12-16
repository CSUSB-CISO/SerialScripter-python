from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
# SQLALCHEMY_TRACK_MODIFICATIONS is deprecated in the latest versions of Flask-SQLAlchemy
# Instead, you can use the Flask-SQLAlchemy event system to track modifications
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'efd9b724cfc5ec69327a2e557108d651 kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///data/{DB_NAME}'
    
    # db.create_all()
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/data/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
