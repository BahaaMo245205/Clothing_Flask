from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from Flask_app import admin, db, bcrypt
from Flask_app.Model import User, Product
from Flask_app.Admin.forms import ProductForm
from flask_admin.contrib.fileadmin import FileAdmin
from Flask_app.Admin.helper import save_picture
import os


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.Type_user == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("Auth_bp.Login"))


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if current_user.is_authenticated:
            if current_user.Type_user == "admin":
                return self.render("admin_html/analytics_index.html", title="Admin")
            else:
                return redirect(url_for("Main_bp.Home"))
        else:
            return redirect(url_for("Auth_bp.Login"))

    @expose("/add_product", methods=["POST", "GET"])
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


    @expose("/DeleteProduct/<int:id>", methods=["GET", "POST"])
    def delete_product(self, id):
        if current_user.Type_user != "admin":
            abort(403)

        deleteProduct = Product.query.get_or_404(id)
        image_filename = deleteProduct.Image
        image_path = os.path.join("Flask_app","static", "Images", "Images_Product", image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
        else :
            print("not found the file")
        db.session.delete(deleteProduct)
        db.session.commit()
        flash("تم الحذف بنجاح", "success")
        return redirect(url_for("admin.add_product"))


    @expose("/UpdateProduct/<int:id>", methods=["GET", "POST"])
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
                image_path = os.path.join("Flask_app", "static", "Images", "Images_Product", product.Image)
                if os.path.exists(image_path):
                    os.remove(image_path)
                product.Image = save_picture(form.Image.data)

            db.session.commit()
            flash("تم التحديث بنجاح", 'success')
            return redirect(url_for("admin.add_product"))

        if request.method == "GET":
            form.name.data = product.ProductName
            form.description.data = product.Description
            form.price.data = product.Price
            form.StockQuantity.data = product.StockQuantity
            form.Category.data = product.Category

        return self.render("admin_html/AddProduct.html", form=form, products=Product.query.all(), is_update=True)


class UserView(MyModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.Type_user == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("Auth_bp.Login"))


adminbp = Blueprint("adminbp", __name__)
