from flask import Flask
from config import Config

from website.routes.admin import admin
from website.routes.auth import auth
from website.routes.clerk import clerk

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(clerk)

    return app