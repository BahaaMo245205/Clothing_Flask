from flask import *
from flask_login import current_user
from Flask_app import bcrypt, db
from Flask_app.Model import *
from Flask_app.user.forms import *
from Flask_app.user.helper import *

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/Profile", methods=["GET", "POST"])
def Profile():
    return render_template("/User_html/Profile.html")


@user_bp.route("/UpdateProfile", methods=["GET", "POST"])
def UpdateProfile():
    form = UpdateInformationUser()

    if request.method == "GET":
        form.FirstName.data = current_user.FirstName
        form.LastName.data = current_user.LastName
        if current_user.information:
            form.Phone.data = str(current_user.information.Phone)
            form.Governorate.data = current_user.information.Governorate
            form.City.data = current_user.information.City
            form.Street.data = current_user.information.Street

    if request.method == "POST":
        if form.validate_on_submit():
            if form.Image.data:
                picture_file = save_picture(form.Image.data)
                current_user.Image = picture_file
            current_user.FirstName = form.FirstName.data
            current_user.LastName = form.LastName.data
            if not current_user.information:
                current_user.information = InformationUser(UserID=current_user.UserID)
                db.session.add(current_user.information)
            current_user.information.Phone = int(form.Phone.data)
            current_user.information.Governorate = form.Governorate.data
            current_user.information.City = form.City.data
            current_user.information.Street = form.Street.data
            db.session.commit()
            flash("تم التعديل بنجاح", "success")
            return redirect(url_for("user_bp.UpdateProfile"))
    return render_template("/User_html/UpdateProfile.html", form=form)


@user_bp.route("/UpdatePassword", methods=["GET", "POST"])
def UpdatePassword():
    form = ChangePasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            current_user.Password = bcrypt.generate_password_hash(form.NewPassword.data)
            db.session.commit()
            flash("تم تغيير كلمة المرور بنجاح", "success")
            return redirect(url_for("user_bp.UpdatePassword"))
        else:
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(f"{err_msg[0]}", "danger")

    return render_template("/User_html/UpdatePassword.html", form=form)


@user_bp.route("/Information", methods=["GET", "POST"])
def Information():
    form = AddInformationUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            info = InformationUser(
                UserID=current_user.UserID,
                Phone=int(form.Phone.data),
                Governorate=form.Governorate.data,
                City=form.City.data,
                Street=form.Street.data,
            )
            db.session.add(info)
            db.session.commit()
            flash("تم أضافة البيانات", "success")
            return redirect(url_for("user_bp.Information"))

    return render_template("/User_html/Information.html", form=form)
