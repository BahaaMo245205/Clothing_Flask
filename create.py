from run import app
from Flask_app.Model import db


with app.app_context():
    db.create_all()