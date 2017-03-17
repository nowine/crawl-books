# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from config import config

admin = Admin(template_mode = 'bootstrap3')
#login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    admin.init_app(app)
#    login_manager.init_app(app)
#    login_manager.login_view = 'auth.login'
    Bootstrap(app)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .main import main
    app.register_blueprint(main)

    return app
