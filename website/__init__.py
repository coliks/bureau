from flask import Flask
from config import Config
from .services.database_init import init_db
from flask_login import LoginManager

from website.routes.admin import admin
from website.routes.auth import auth
from website.routes.clerk import clerk
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    try:
        init_db()
    except Exception as e:
        print("Error: ",e)

    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(clerk)

    return app