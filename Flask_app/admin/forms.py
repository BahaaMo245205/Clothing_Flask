from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    IntegerField,
    SearchField,
)


class ProductForm(FlaskForm):
    Image = FileField(
        "صورة المنتج",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "jpeg"], "الصور فقط مسموح بها!"),
        ],
    )
    name = StringField("أسم المنتج", validators=[DataRequired()])
    description = TextAreaField("الوصف", validators=[DataRequired()])
    price = IntegerField("سعر المنتج", validators=[DataRequired()])
    StockQuantity = IntegerField("الكمية المتاحة", validators=[DataRequired()])
    Category = SelectField(
        "الفئة", choices=["صيفي", "شتوي"], validators=[DataRequired()]
    )
    submit = SubmitField("submit")


class Analyices_projectForm(FlaskForm):
    search = SearchField("بحث", validators=[DataRequired()])
    submit = SubmitField("submit")
