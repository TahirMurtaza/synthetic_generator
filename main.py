from flask import Flask
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
   
    from app.models import User
   
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    
    
    # blueprint for auth routes in our app
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.main import home as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app

app = create_app()