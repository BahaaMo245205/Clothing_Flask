import secrets
import os
from PIL import Image
from flask import current_app

app = current_app


def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/images/Images_Product", picture_name)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_name
