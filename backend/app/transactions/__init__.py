from flask import Blueprint
from .models import income_expense_item

# "transactions" Blueprintの定義。
transactions_blueprint = Blueprint('transactions', __name__)

# routesなど、transactionsパッケージ内の他のモジュールをインポートします。
from . import routes
