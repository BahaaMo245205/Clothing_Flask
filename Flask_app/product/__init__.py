from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    session,
)
from Flask_app.Model import Product, Booking, InformationUser, InformationBooking
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user, login_required
from Flask_app.Admin.helper import save_picture
from flask_wtf import FlaskForm
from Flask_app import db
from wtforms import (
    SubmitField,
    IntegerField,
)


class BookingProductForm(FlaskForm):
    StockQuantity = IntegerField("الكمية المطلوبة", validators=[DataRequired()])
    submit = SubmitField("حجزر المنتج")

    def validate_StockQuantity(self, StockQuantity):
        if StockQuantity.data <= 0:
            raise ValidationError("يجب اختيار عدد صحيح يزيد عن صفر")


product_pb = Blueprint("product_pb", __name__)


@product_pb.route("/Basket", methods=["GET", "POST"])
@login_required
def show_basket():
    basket = session.get("Basket", {})

    if not isinstance(basket, dict):
        basket = {}

    products_to_show = []
    total_price = 0

    for p_id, quantity in basket.items():
        product = Product.query.get(int(p_id))

        if product:
            item_total = product.Price * quantity
            total_price += item_total

            products_to_show.append(
                {"info": product, "quantity": quantity, "total": item_total}
            )
    print(dict(session))
    return render_template(
        "/Product_html/basket.html", products=products_to_show, total=total_price
    )


@product_pb.route("/Booking", methods=["GET", "POST"])
@login_required
def Booking_():
    basket = session.get("Basket", {})
    if not isinstance(basket, dict) or not basket:
        flash("سلة التسوق فارغة", "info")
        return redirect(url_for("Main_bp.index"))

    for id_p, quantity in basket.items():
        product = Product.query.get(int(id_p))
        if not product or quantity > product.StockQuantity:
            name = product.ProductName if product else f"ID: {id_p}"
            flash(f"عذراً، الكمية المطلوبة للمنتج '{name}' غير متوفرة حالياً", "danger")
            return redirect(url_for("product_pb.show_basket"))

    booking = Booking(UserID=current_user.UserID)
    db.session.add(booking)
    db.session.flush()

    try:
        for p_id, quantity in basket.items():
            booking_detail = InformationBooking(
                BookingID=booking.BookingID,
                ProductID=int(p_id),
                Quantity=int(quantity),
                Price=float(Product.query.get(int(p_id)).Price),
                UserID=current_user.UserID,
            )
            db.session.add(booking_detail)

            product = Product.query.get(quantity)
            if product:
                product.StockQuantity -= quantity

        db.session.commit()
        session.pop("Basket", None)
        flash("تم الحجز بنجاح", "success")
        return redirect(url_for("Main_bp.index"))

    except Exception as e:
        db.session.rollback()
        flash("حدث خطأ أثناء تسجيل الحجز، حاول مرة أخرى.", "danger")
        return redirect(url_for("main.cart"))


@product_pb.route("/DeleteFromBasket/<int:id>", methods=["GET", "POST"])
@login_required
def DeleteFromBasket(id):
    basket = session.get("Basket", {})
    if not isinstance(basket, dict):
        basket = {}

    if str(id) in basket:
        del basket[str(id)]
        session["Basket"] = basket
        session.modified = True

    return redirect(url_for("product_pb.show_basket"))


@product_pb.route("/BookingProduct/<int:id>", methods=["GET", "POST"])
@login_required
def AddInBasket(id):
    product = Product.query.get_or_404(id)
    informationUser = InformationUser.query.filter_by(
        UserID=current_user.UserID
    ).first()

    form = BookingProductForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if not informationUser:
                flash("الرجاء تسجيل البيانات الشخصية أولاً", "danger")
                return redirect(url_for("user_bp.Information"))

            stock_quantity = form.StockQuantity.data
            if stock_quantity <= product.StockQuantity:

                basket = session.get("Basket")

                if not isinstance(basket, dict):
                    basket = {}

                p_id = str(product.ProductID)

                if p_id in basket:
                    basket[p_id] += stock_quantity
                else:
                    basket[p_id] = stock_quantity

                session["Basket"] = basket
                session.modified = True

                flash(f"تم إضافة {product.ProductName} لقائمة الحجز", "success")
                return redirect(url_for("Main_bp.index"))

            else:
                flash("الكمية المطلوبة غير متوفرة في المخزن حالياً", "danger")
                return redirect(url_for("Main_bp.index"))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"خطأ في {field}: {error}", "danger")

    return render_template(
        "/Product_html/info_product.html", product=product, form=form
    )
