from . import db
from sqlalchemy.orm import backref

class IncomeExpenseItem(db.Model):
    __tablename__ = 'income_expense_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.Enum('income', 'expense'), nullable=False)

    # Relationship
    monthly_records = db.relationship('MonthlyRecord', backref=backref('income_expense_item', lazy=True))
