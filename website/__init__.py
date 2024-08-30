from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HIFUN@1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User, Note

    # Create database if it doesn't exist
    def create_database(app):
        if not path.exists('website/' + DB_NAME):
            with app.app_context():
                db.create_all()
    create_database(app)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Adjust 'auth.login' to your login route
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app