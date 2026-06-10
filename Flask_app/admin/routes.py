from Flask_app.Model import Product, Booking, InformationUser, User, InformationBooking
from flask import Blueprint, request, redirect, url_for, flash, abort, current_app
from Flask_app.Admin.forms import ProductForm, Analyices_projectForm
from flask_login import current_user, login_required
from Flask_app.Admin.helper import save_picture
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from Flask_app import db
import os


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.Type_user == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("Auth_bp.Login"))


class MyAdminIndexView(AdminIndexView):
    ######################################
    @expose("/", methods=["POST", "GET"])
    @login_required
    def index(self):
        if current_user.is_authenticated and current_user.Type_user == "admin":
            form = Analyices_projectForm()
            search_query = (
                request.args.get("search").strip()
                if request.args.get("search")
                else None
            )
            query = Booking.query.join(User).join(
                InformationUser, User.UserID == InformationUser.UserID
            )
            if search_query:
                query = query.filter(
                    (Booking.BookingID == search_query)
                    | (User.FirstName.like(f"%{search_query}%"))
                    | (User.LastName.like(f"%{search_query}%"))
                    | (InformationUser.Governorate.like(f"%{search_query}%"))
                )
            bookings = query.all()
            num_TotalBooking = Booking.query.count()
            WaitBooking = Booking.query.filter_by(deliver_booking="No").all()
            DoneBooking = Booking.query.filter_by(deliver_booking="Yes").all()
            informationbooking = InformationUser.query.all()
            return self.render(
                "admin_html/analytics_index.html",
                title="Admin",
                form=form,
                bookings=bookings,
                num_TotalBooking=num_TotalBooking,
                num_deliver=len(WaitBooking),
                num_DoneBooking=len(DoneBooking),
                num_InformationUser=len(informationbooking),
            )
        else:
            return redirect(url_for("Auth_bp.Login"))

    ######################################

    @expose("/booking_details/<int:id>", methods=["POST", "GET"])
    @login_required
    def booking_details(self, id):
        GetProducts = InformationBooking.query.filter_by(BookingID=id).all()
        if request.method == "POST":
            ChickOrder = Booking.query.get_or_404(id)
            ChickOrder.deliver_booking = "Yes"
            flash("تم تسليم بي نجاح", "success")
            db.session.commit()
            return redirect(url_for("admin.index"))

        return self.render("/admin_html/booking_details.html", products=GetProducts)

    @expose("/add_product", methods=["POST", "GET"])
    @login_required
    def add_product(self):
        form = ProductForm()
        if request.method == "POST":
            if form.validate_on_submit():
                Name = form.name.data
                Description = form.description.data
                Price = form.price.data
                StockQuantity = form.StockQuantity.data
                Category = form.Category.data
                Image = form.Image.data
                if Image:
                    product = Product(
                        ProductName=Name,
                        Description=Description,
                        Price=Price,
                        StockQuantity=StockQuantity,
                        Category=Category,
                        Image=save_picture(Image),
                    )
                    db.session.add(product)
                    db.session.commit()
                    flash("تم إضافة المنتج بنجاح", "success")
                    return redirect(url_for("admin.add_product"))

        return self.render(
            "admin_html/AddProduct.html", form=form, products=Product.query.all()
        )

    ########################################################
    @expose("/DeleteProduct/<int:id>", methods=["GET", "POST"])
    @login_required
    def delete_product(self, id):
        if current_user.Type_user != "admin":
            abort(403)

        product = Product.query.get_or_404(id)

        undelivered = (
            db.session.query(InformationBooking)
            .join(Booking)
            .filter(InformationBooking.ProductID == id, Booking.deliver_booking == "No")
            .first()
        )

        if undelivered:
            flash("لا يمكن حذف المنتج لأنه مرتبط بحجوزات لم يتم تسليمها بعد", "danger")
            return redirect(url_for("admin.add_product"))

        InformationBooking.query.filter_by(ProductID=id).delete()

        if product.Image:
            image_path = os.path.join(
                current_app.root_path,
                "static",
                "images",
                "Images_Product",
                product.Image,
            )
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(product)
        db.session.commit()
        flash("تم الحذف بنجاح", "success")
        return redirect(url_for("admin.add_product"))

    ########################################################

    @expose("/UpdateProduct/<int:id>", methods=["GET", "POST"])
    @login_required
    def update_product(self, id):
        if current_user.Type_user != "admin":
            abort(403)

        product = Product.query.get_or_404(id)
        form = ProductForm()

        if form.validate_on_submit():
            product.ProductName = form.name.data
            product.Description = form.description.data
            product.Price = form.price.data
            product.StockQuantity = form.StockQuantity.data
            product.Category = form.Category.data

            if form.Image.data:
                image_path = os.path.join(
                    "Flask_app", "static", "Images", "Images_Product", product.Image
                )
                if os.path.exists(image_path):
                    os.remove(image_path)
                product.Image = save_picture(form.Image.data)

            db.session.commit()
            flash("تم التحديث بنجاح", "success")
            return redirect(url_for("admin.add_product"))

        if request.method == "GET":
            form.name.data = product.ProductName
            form.description.data = product.Description
            form.price.data = product.Price
            form.StockQuantity.data = product.StockQuantity
            form.Category.data = product.Category
            form.Image.data = product.Image

        return self.render(
            "admin_html/AddProduct.html",
            form=form,
            products=Product.query.all(),
            is_update=True,
        )


class UserView(MyModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.Type_user == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("Auth_bp.Login"))


adminbp = Blueprint("adminbp", __name__)
