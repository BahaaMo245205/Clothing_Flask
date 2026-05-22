from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_user, logout_user, login_required, current_user


Main_bp = Blueprint("Main_bp", __name__)

@Main_bp.route("/")
def index():
    return render_template("main_html/index.html")


@Main_bp.route("/about")
def about():
    return render_template("main_html/about.html")