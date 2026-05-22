from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db) # السطر ده هو اللي بيفعل أمر db

    from Flask_app.main.routes import Main_bp
    app.register_blueprint(Main_bp)

    from Flask_app.auth.routes import Auth_bp
    app.register_blueprint(Auth_bp)

    return app