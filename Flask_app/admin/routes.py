from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from Flask_app import admin, db, bcrypt
from Flask_app.Model import User, Product
from Flask_app.Admin.forms import ProductForm
from flask_admin.contrib.fileadmin import FileAdmin
from Flask_app.Admin.helper import save_picture




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
                    product = Product(ProductName=Name, Description=Description, Price=Price, StockQuantity=StockQuantity, Category=Category, Image=save_picture(Image))
                    db.session.add(product)
                    db.session.commit()
                    flash("تم إضافة المنتج بنجاح", "success")
                    return redirect(url_for("admin.add_product"))
                
        return self.render("admin_html/AddProduct.html", form=form)



class UserView(MyModelView):
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.Type_user == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("Auth_bp.Login"))


adminbp = Blueprint("adminbp", __name__)

