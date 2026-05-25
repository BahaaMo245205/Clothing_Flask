from flask import Blueprint, render_template, redirect, url_for, flash, request
from Flask_app.auth.form import (
    LoginForm,
    UserResgister,
    ForgetPasswordForm,
    ResetPasswordForm,
)
from Flask_app.auth.Helper import sent_email
from Flask_app import db, bcrypt
from Flask_app.Model import User
from flask_login import login_user, logout_user, login_required, current_user

Auth_bp = Blueprint("Auth_bp", __name__)


@Auth_bp.route("/Register", methods=["GET", "POST"])
def Register():
    form = UserResgister()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                FirstName=form.FirstName.data.strip(),
                LastName=form.LastName.data.strip(),
                Email=form.email.data.strip(),
                Password=hashed_password.strip(),
            )
            db.session.add(user)
            db.session.commit()
            flash("تم التسجيل بنجاح", "success")
            return redirect(url_for("Auth_bp.Login"))
        else:
            if form.errors != {}:
                for err_msg in form.errors.values():

                    flash(f"حاول مرة اخرى{err_msg}", "danger")
    return render_template("auth_html/Register.html", form=form, title="تسجيل")


@Auth_bp.route("/Login", methods=["GET", "POST"])
def Login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(Email=form.email.data.strip()).first()
            if user and bcrypt.check_password_hash(user.Password, form.password.data):
                login_user(user)
                flash("تم تسجيل الدخول بنجاح", "success")
                return redirect(url_for("Main_bp.index"))
            else:
                if form.errors != {}:
                    for err_msg in form.errors.values():
                        flash(f"حاول مرة اخرى{err_msg}", "danger")
    return render_template("auth_html/Login.html", form=form)


@Auth_bp.route("/ForgetPassword", methods=["GET", "POST"])
def ForgetPassword():
    form = ForgetPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(Email=form.email.data.strip()).first()
            sent_email(user)
            flash("تم ارسال البريد بنجاح", "success")
            return redirect(url_for("Auth_bp.Login"))
    return render_template("auth_html/forget_password.html", form=form)


@Auth_bp.route("/ResetPassword/<path:token>", methods=["GET", "POST"])
def ResetPassword(token):
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for("Main_bp.index"))
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.verify_reset_token(token)
            if not user:
                flash("Invalid or expired token", "warning")
                return redirect(url_for("Auth_bp.ForgetPassword"))
            if user:
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data
                ).decode("utf-8")
                user.Password = hashed_password
                db.session.commit()
                flash(
                    "Your password has been updated! You are now able to log in",
                    "success",
                )
                return redirect(url_for("Auth_bp.Login"))
            else:
                flash("Invalid or expired token", "warning")
                return redirect(url_for("Auth_bp.ForgetPassword"))

    return render_template("auth_html/reset_password.html", form=form)


@Auth_bp.route("/Logout")
@login_required
def Logout():
    logout_user()
    return redirect(url_for("Main_bp.index"))
