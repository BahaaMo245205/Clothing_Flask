from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError
from Flask_app.Model import User


class LoginForm(FlaskForm):
    email = StringField("الإيميل", validators=[DataRequired(), Email()])
    password = PasswordField(
        "كلمة المرور", validators=[DataRequired(), Length(min=6, max=20)]
    )

    submit = SubmitField("تسجيل الدخول")


class UserResgister(FlaskForm):
    FirstName = StringField("الاسم الاول", validators=[DataRequired()])
    LastName = StringField("الاسم الاخير", validators=[DataRequired()])
    email = StringField("الإيميل", validators=[DataRequired(), Email()])
    password = StringField(
        "كلمة المرور", validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirm_password = StringField(
        "تأكيد كلمة المرور", validators=[DataRequired(), Length(min=6, max=20)]
    )
    submit = SubmitField("تسجيل")

    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user:
            raise ValidationError("هذا الايميل مستخدم من قبل")

    def validate_password(self, password):
        if password.data != self.confirm_password.data:
            raise ValidationError("كلمة المرور غير متطابقة")


class ForgetPasswordForm(FlaskForm):
    email = StringField("الإيميل", validators=[DataRequired(), Email()])
    submit = SubmitField("استعادة كلمة المرور")


class ResetPasswordForm(FlaskForm):
    NewPassword = StringField(
        "كلمة المرور الجديدة", validators=[DataRequired(), Length(min=6, max=20)]
    )
    ConfirmNewPassword = StringField(
        "تأكيد كلمة المرور الجديدة", validators=[DataRequired(), Length(min=6, max=20)]
    )
    submit = SubmitField("تعيين كلمة المرور الجديدة")
