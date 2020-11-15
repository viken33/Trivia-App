from flask import Flask
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_principal import Principal
from flask_migrate import Migrate
import os

login_manager = LoginManager()
db = SQLAlchemy()
admin = Admin()
principal = Principal()
migrate = Migrate()


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
    POSTGRES = {
        'user': 'postgres',
        'pw': 'postgres',
        'db': 'trivia',
        'host': 'localhost',
        'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES['user']}:" \
                           f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                           f"{POSTGRES['port']}/{POSTGRES['db']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    principal.init_app(app)
    # Se inicializa el objeto migrate
    migrate.init_app(app, db)

    # Registro de los Blueprints
    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .restricted import restricted_bp
    app.register_blueprint(restricted_bp)

    return app







