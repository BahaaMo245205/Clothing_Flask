from flask import Blueprint, render_template, redirect, url_for, flash,request
from Flask_app.auth.form import LoginForm, UserResgister
from Flask_app import db
from Flask_app.Model import User
from flask_login import login_user, logout_user, login_required, current_user


Auth_bp = Blueprint("Auth_bp", __name__)


@Auth_bp.route("/Register", methods=["GET", "POST"])
def Register():
    form = UserResgister()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                form.FirstName.data,
                form.LastName.data,
                form.email.data,
                form.passowrd.data,
            )
            if user :
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("Auth_bp.Login"))
    return render_template("auth_html/Register.html", form=form)


@Auth_bp.route("/Login", methods=["GET", "POST"])
def Login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.Password == form.password.data:
                login_user(user)
                return redirect(url_for("Main_bp.index"))
    return render_template("auth_html/Login.html", form=form)


@Auth_bp.route("/Logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for("Main_bp.index"))