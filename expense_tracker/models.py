from expense_tracker import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(255))
    password_hash = db.Column('password', db.String(255))  
    firstname = db.Column('firstname', db.String(255))
    lastname = db.Column('lastname', db.String(255)) 
    email = db.Column('email', db.String(255)) 
    isAdmin = db.Column(db.Boolean, default=False) 
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade="all, delete") 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    @property
    def password(self):
        raise AttributeError('Password incorrect') 
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<User: {self.username}>'


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    category = db.Column(db.String(255)) 
    description = db.Column(db.String(255))  
    date = db.Column(db.Date) 
    amount = db.Column(db.Float(50)) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Category: {self.category}>'

 #renanmed modal