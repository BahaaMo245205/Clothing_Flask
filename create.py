from run import app
from flask import session
from Flask_app.Model import db


with app.app_context():
    db.create_all()
    