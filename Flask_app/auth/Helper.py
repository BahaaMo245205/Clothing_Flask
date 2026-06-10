from flask_login import current_user
from flask_mail import Message
from Flask_app import mail
from config import Config
from flask import url_for


def sent_email(user):
    token = user.get_reset_token()
    msg = Message(subject="تغيير كلمة المرور - متجر شياكة", recipients=[user.Email])

    link = url_for("Auth_bp.ResetPassword", token=token, _external=True)

    msg.body = f"""أهلاً {user.FirstName}،

لتغيير كلمة المرور الخاصة بحسابك في متجر شياكة، يرجى الضغط على الرابط التالي:
{link}

إذا لم تطلب تغيير كلمة المرور، يرجى تجاهل هذا الإيميل.
"""
    mail.send(msg)
