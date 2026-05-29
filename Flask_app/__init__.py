from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
admin = Admin( name='شياكة Store')

login_manager.login_view = "Auth_bp.Login"
login_manager.login_message_category = "info"



def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    from Flask_app.Admin.routes import MyAdminIndexView


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app,index_view=MyAdminIndexView())

    from Flask_app.main.routes import Main_bp
    from Flask_app.auth.routes import Auth_bp
    from Flask_app.Admin.routes import adminbp
    from Flask_app.user.routes import user_bp


    app.register_blueprint(Main_bp)
    app.register_blueprint(Auth_bp)
    app.register_blueprint(adminbp)
    app.register_blueprint(user_bp)
    
    return app
