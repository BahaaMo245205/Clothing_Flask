from flask import Blueprint, render_template, redirect, url_for, flash,request
from Flask_app.Model import Product

Main_bp = Blueprint("Main_bp", __name__)

@Main_bp.route("/")
def index():
    products = Product.query.all()
    return render_template("main_html/index.html", products=products)


@Main_bp.route("/about")
def about():
    return render_template("main_html/about.html")