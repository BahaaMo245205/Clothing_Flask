import secrets

import os

from PIL import Image

from flask import current_app

app = current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    

    picture_path = os.path.join(app.root_path, 'static', 'Images', 'Images_user', picture_name)
    
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name