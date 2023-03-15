from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Nishad212000@127.0.0.1:3306/login_store'
app.config['SECRET_KEY'] = 'Admin_pwd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.username'), unique=True)

    gender = db.Column(db.String(6), nullable=False)
    married = db.Column(db.String(20), nullable=False)
    dependents = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(20), nullable=False)
    self_employed = db.Column(db.String(10), nullable=False)
    applicantincome = db.Column(db.Integer, nullable=False)
    coapplicantincome = db.Column(db.Integer, nullable=False)
    loanamount = db.Column(db.Integer, nullable=False)
    loan_amount_term = db.Column(db.Integer, nullable=False)
    credit_history = db.Column(db.String(20), nullable=False)
    property_area = db.Column(db.String(20), nullable=False)
    applicationStatus = db.Column(db.String(20), nullable=False)


db.create_all()