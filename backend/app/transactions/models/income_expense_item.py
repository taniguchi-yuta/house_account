from . import db
from sqlalchemy.orm import backref
from ...models.mixins import TimestampMixin

class IncomeExpenseItem(db.Model, TimestampMixin):
    __tablename__ = 'income_expense_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.Enum('income', 'expense'), nullable=False)
    transaction_day = db.Column(db.Integer)  # 追加：毎月の支払い日（1日から31日）
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationship
    monthly_records = db.relationship('MonthlyRecord', backref=backref('income_expense_item', lazy=True))
