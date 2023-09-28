from datetime import datetime
from . import db
from sqlalchemy.orm import backref

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    regist_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    income_expense_items = db.relationship('IncomeExpenseItem', backref=backref('user', lazy=True))
    monthly_records = db.relationship('MonthlyRecord', backref=backref('user', lazy=True))
