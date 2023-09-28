from . import db

class MonthlyRecord(db.Model):
    __tablename__ = 'monthly_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    income_expense_item_id = db.Column(db.Integer, db.ForeignKey('income_expense_items.id'), nullable=False)
    month = db.Column(db.String(6), nullable=False)  # YYYYMM format
    amount = db.Column(db.Numeric, nullable=False)
