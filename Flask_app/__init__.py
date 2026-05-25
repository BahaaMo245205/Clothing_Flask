from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = "Auth_bp.Login"
login_manager.login_message_category = "info"



def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from Flask_app.main.routes import Main_bp

    app.register_blueprint(Main_bp)

    from Flask_app.auth.routes import Auth_bp

    app.register_blueprint(Auth_bp)

    return app
