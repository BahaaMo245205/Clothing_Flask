from flask_login import UserMixin
from Flask_app import db, login_manager
from itsdangerous import URLSafeTimedSerializer, Serializer
from flask import current_app


class User(db.Model, UserMixin):
    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Type_user = db.Column(db.String(50), nullable=False, default="user")

    def get_id(self):
        return str(self.UserID)

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.UserID})

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=age)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.FirstName}','{self.LastName}','{self.Email}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Price = db.Column(db.Float, nullable=False)
    StockQuantity = db.Column(db.Integer, default=0)
    Category = db.Column(db.String(50), nullable=True)


Booking = db.Table(
    "Booking",
    db.Column("BookingID", db.Integer, primary_key=True),
    db.Column("UserID", db.Integer, db.ForeignKey("user.UserID"), primary_key=True),
    db.Column(
        "ProductID", db.Integer, db.ForeignKey("product.ProductID"), primary_key=True
    ),
    db.Column("BookingDate", db.DateTime, nullable=False),
    db.Column("Quantity", db.Integer, nullable=False),
)
