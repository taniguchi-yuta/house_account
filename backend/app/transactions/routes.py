from flask import jsonify, request
from flask_login import current_user, login_required
from .models.income_expense_item import IncomeExpenseItem
from .models.monthly_record import MonthlyRecord
from .models import db
from . import transactions_blueprint
from sqlalchemy import and_

@transactions_blueprint.route('/api/v1/transactions/item', methods=['POST'])
@login_required
def add_item():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    item_type = request.json.get('ItemType', None)
    item_name = request.json.get('ItemName', None)

    if not item_type or item_type not in ['income', 'expense']:
        return jsonify({"status": "error", "message": "Invalid or missing ItemType parameter"}), 400
    if not item_name:
        return jsonify({"status": "error", "message": "Missing ItemName parameter"}), 400

    user_id = current_user.id

    new_item = IncomeExpenseItem(user_id=user_id, item_name=item_name, item_type=item_type)
    
    new_item.created_by = user_id
    new_item.updated_by = user_id
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"status": "success", "message": "Item added successfully!"}), 201


@transactions_blueprint.route('/api/v1/transactions/item/<int:item_id>', methods=['PUT'])
@login_required
def update_transaction_item(item_id):
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    item_type = request.json.get('ItemType')
    item_name = request.json.get('ItemName')

    if not any([item_type, item_name]):
        return jsonify({"status": "error", "message": "Provide at least one parameter to update (ItemType or ItemName)"}), 400

    item = IncomeExpenseItem.query.get(item_id)
    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    if item.user_id != current_user.id:
        return jsonify({"status": "error", "message": "You are not authorized to update this item"}), 403

    if item_type:
        if item_type not in ['income', 'expense']:
            return jsonify({"status": "error", "message": "Invalid ItemType parameter"}), 400
        item.item_type = item_type

    if item_name:
        item.item_name = item_name

    item.update_by = current_user.id
    db.session.commit()

    return jsonify({"status": "success", "message": "Transaction item updated successfully!"}), 200


@transactions_blueprint.route('/api/v1/transactions/items', methods=['GET'])
@login_required
def get_items():
    user_id = current_user.id

    # ユーザーIDに基づいて入出金事項を取得
    items = IncomeExpenseItem.query.filter_by(user_id=user_id).all()

    # オブジェクトのリストを辞書のリストに変換
    items_list = [{
        "id": item.id,
        "item_name": item.item_name,
        "item_type": item.item_type,
        "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # assuming created_at is a datetime field
        "updated_at": item.updated_at.strftime('%Y-%m-%d %H:%M:%S')   # assuming updated_at is a datetime field
    } for item in items]

    return jsonify({"status": "success", "items": items_list}), 200


@transactions_blueprint.route('/api/v1/transactions/monthly', methods=['POST'])
@login_required
def add_monthly_transaction():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    month = request.json.get('Month')
    amount = request.json.get('Amount')
    item_name = request.json.get('ItemName')

    if not month or not amount or not item_name:
        return jsonify({"status": "error", "message": "Missing required parameters (Month, Amount, ItemName)"}), 400

    user_id = current_user.id
    item = IncomeExpenseItem.query.filter_by(item_name=item_name, user_id=user_id).first()

    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404

    new_record = MonthlyRecord(
        user_id=user_id,
        income_expense_item_id=item.id,
        month=month,
        amount=amount
    )

    db.session.add(new_record)
    db.session.commit()

    return jsonify({"status": "success", "message": "Monthly transaction added successfully!"}), 201


@transactions_blueprint.route('/api/v1/transactions/monthly/<int:transaction_id>', methods=['PUT'])
@login_required
def update_monthly_transaction(transaction_id):
    # 取引をDBから取得
    record = MonthlyRecord.query.filter_by(id=transaction_id, user_id=current_user.id).first()

    if not record:
        return jsonify({"status": "error", "message": "Transaction not found"}), 404

    # リクエストからデータを取得
    data = request.get_json()
    month = data.get("Month")
    amount = data.get("Amount")
    item_name = data.get("ItemName")

    if item_name:
        item = IncomeExpenseItem.query.filter_by(item_name=item_name, user_id=current_user.id).first()
        if not item:
            return jsonify({"status": "error", "message": "Item not found"}), 400
        record.income_expense_item_id = item.id

    # 月、金額、アイテム名を更新
    if month:
        record.month = month
    if amount:
        record.amount = amount

    # DBに変更をコミット
    db.session.commit()

    return jsonify({"status": "success", "message": "Transaction updated successfully"}), 200


@transactions_blueprint.route('/api/v1/transactions/monthly', methods=['GET'])
@login_required
def get_monthly_transactions():
    month = request.args.get('month') # クエリパラメータから月を取得
    user_id = current_user.id

    if month:
        # 月が指定された場合、その月の入出金のみを取得
        transactions = MonthlyRecord.query.filter(and_(MonthlyRecord.user_id == user_id, MonthlyRecord.month == month)).all()
    else:
        # 月が指定されていない場合、全ての入出金を取得
        transactions = MonthlyRecord.query.filter_by(user_id=user_id).all()

    transactions_list = [{
        "id": transaction.id,
        "month": transaction.month,
        "amount": str(transaction.amount),  # Numeric type needs to be converted to string for JSON serialization
        "item_name": IncomeExpenseItem.query.get(transaction.income_expense_item_id).item_name  # Assuming there's a related model for item name
    } for transaction in transactions]

    return jsonify({"transactions": transactions_list}), 200