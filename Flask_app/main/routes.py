from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from Flask_app.Model import Product, InformationUser

Main_bp = Blueprint("Main_bp", __name__)


@Main_bp.route("/")
def index():
    products = Product.query.all()
    num_basket = session.get("Basket")
    return render_template(
        "main_html/index.html",
        products=products,
        num_basket=len(num_basket) if num_basket else 0,
    )


@Main_bp.route("/about")
def about():
    return render_template("main_html/about.html")
