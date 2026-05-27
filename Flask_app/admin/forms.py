from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,SelectField,IntegerField
from wtforms.validators import DataRequired


class ProductForm (FlaskForm):
    Image = FileField('صورة المنتج', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'],'الصور فقط مسموح بها!')])
    name = StringField('أسم المنتج', validators=[DataRequired()])
    description = TextAreaField("الوصف",validators=[DataRequired()])
    price = IntegerField('سعر المنتج', validators=[DataRequired()])
    StockQuantity = IntegerField('الكمية المتاحة', validators=[DataRequired()])
    Category = SelectField('الفئة', choices=["صيفي","شتوي"], validators=[DataRequired()])
    submit = SubmitField('submit')