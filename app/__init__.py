from flask import Flask
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__, static_folder=None)
    app.static_url_path = '/static'

    with app.app_context():
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)

        db.init_app(app)
        login_manager.init_app(app)
        bootstrap.init_app(app)

        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint, url_prefix="/")

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix="/auth")

        from .antragsteller import antragsteller as antragsteller_blueprint
        app.register_blueprint(antragsteller_blueprint, url_prefix="/antragsteller")

        from .behoerde import behoerde as behoerde_blueprint
        app.register_blueprint(behoerde_blueprint, url_prefix="/behoerde")

        from .common import bauantrag as bauantrag_blueprint
        app.register_blueprint(bauantrag_blueprint, url_prefix="/bauantrag")

        mail.init_app(app)

    return app
