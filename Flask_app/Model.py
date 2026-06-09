from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from Flask_app import db, login_manager
from itsdangerous import URLSafeTimedSerializer


class User(db.Model, UserMixin):
    __tablename__ = "user"
    UserID = db.Column(db.Integer, primary_key=True)
    Image = db.Column(db.String(100), nullable=True, default="default.jpg")
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Type_user = db.Column(db.String(50), nullable=False, default="user")

    information = db.relationship(
        "InformationUser", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    bookings = db.relationship("Booking", backref="client", lazy=True)

    def get_id(self):
        return str(self.UserID)

    def get_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.UserID}, salt="password-reset-salt")

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token, salt="password-reset-salt", max_age=age)
            user_id = data["user_id"]
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.FirstName}','{self.LastName}','{self.Email}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class InformationUser(db.Model):
    __tablename__ = "information_user"
    InformationID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(
        db.Integer,
        db.ForeignKey("user.UserID", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    Phone = db.Column(db.String(15), nullable=False)
    Governorate = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    Street = db.Column(db.String(50), nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100), nullable=False)
    Image = db.Column(db.String(100), nullable=True)
    Description = db.Column(db.Text, nullable=True)
    Price = db.Column(db.Float, nullable=False)
    StockQuantity = db.Column(db.Integer, default=0)
    Category = db.Column(db.String(50), nullable=True)
    DateProduct = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Booking(db.Model):
    __tablename__ = "Booking"
    BookingID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey("user.UserID"), nullable=False)
    BookingDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deliver_booking = db.Column(
        db.String(10), nullable=True, default="No"
    )  # "No" أو "Yes"
    
    details = db.relationship(
        "InformationBooking",
        backref="main_booking",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Booking('ID: {self.BookingID}', 'User: {self.UserID}', 'Product: {self.ProductID}')"


class InformationBooking(db.Model):
    __tablename__ = "Information_Booking"
    InformationBookingID = db.Column(db.Integer, primary_key=True)
    BookingID = db.Column(
        db.Integer, db.ForeignKey("Booking.BookingID"), nullable=False
    )
    ProductID = db.Column(
        db.Integer, db.ForeignKey("product.ProductID"), nullable=False
    )
    UserID = db.Column(db.Integer, db.ForeignKey("user.UserID"), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float, nullable=False)

    product_info = db.relationship("Product", backref="booked_items")
