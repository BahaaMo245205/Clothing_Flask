from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user, login_required
from Flask_app.Admin.helper import save_picture
from Flask_app.Model import  Product
from flask_wtf import FlaskForm
from Flask_app import db
from wtforms import (
    SubmitField,
    IntegerField,
)
from datetime import datetime



class BookingProductForm(FlaskForm):
    StockQuantity = IntegerField("الكمية المطلوبة", validators=[DataRequired()])
    submit = SubmitField("حجزر المنتج")
    
    def validate_StockQuantity(self, StockQuantity):
        if StockQuantity.data <= 0:
            raise ValidationError("يجب اخطيار عدد صحيح يزيد عن صفر", "danger")


product_pb = Blueprint("product_pb", __name__)


@product_pb.route("/BookingProduct/<int:id>", methods=["GET", "POST"])
@login_required
def BookingProduct(id):
    product = Product.query.get_or_404(id)
    form = BookingProductForm()
    if request.method == "POST":
        if form.validate_on_submit():
            StockQuantity = form.StockQuantity.data
            if StockQuantity <= product.StockQuantity:
                product.StockQuantity -= StockQuantity
                db.session.commit
                flash("تم حجز المنتج بنجاح", "success")
                return redirect(url_for("Main_bp.Home"))
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash(f"{error}", "danger")

    return render_template(
        "/Product_html/info_product.html", product=product, form=form
    )
