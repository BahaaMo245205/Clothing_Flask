from wtforms.validators import *
from Flask_app.Model import User
from Flask_app import db, bcrypt
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import *


class AddInformationUserForm(FlaskForm):
    Phone = StringField(
        "رقم الهاتف", validators=[DataRequired(), Length(min=10, max=10)]
    )
    Governorate = StringField("المحافظة", validators=[DataRequired()])
    City = StringField("المدينة", validators=[DataRequired()])
    Street = StringField("الشارع", validators=[DataRequired()])
    submit = SubmitField("حفظ")


class UpdateInformationUser(FlaskForm):
    Image = FileField(
        "الصورة الشخصية", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    FirstName = StringField("الاسم الاول", validators=[DataRequired()])
    LastName = StringField("الاسم الاخير", validators=[DataRequired()])
    Phone = StringField(
        "رقم الهاتف", validators=[DataRequired(), Length(min=10, max=10)]
    )
    Governorate = StringField("المحافظة", validators=[DataRequired()])
    City = StringField("المدينة", validators=[DataRequired()])
    Street = StringField("الشارع", validators=[DataRequired()])
    submit = SubmitField("حفظ")


class ChangePasswordForm(FlaskForm):
    OldPassword = StringField("كلمة المرور القديمة", validators=[DataRequired()])
    NewPassword = StringField(
        "كلمة المرور الجديدة",
        validators=[
            DataRequired(),
            Length(min=6, max=20),
            EqualTo("ConfirmNewPassword"),
        ],
    )
    ConfirmNewPassword = StringField(
        "تأكيد كلمة المرور الجديدة", validators=[DataRequired()]
    )
    submit = SubmitField("تعيين كلمة المرور الجديدة")

    def validate_OldPassword(self, OldPassword):
        if not bcrypt.check_password_hash(current_user.Password, OldPassword.data):
            raise ValidationError("كلمة المرور القديمة غير صحيحة")
