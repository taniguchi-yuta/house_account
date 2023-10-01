from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .income_expense_item import IncomeExpenseItem
from .monthly_record import MonthlyRecord
