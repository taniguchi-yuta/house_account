from flask import jsonify, request
from flask_login import current_user, login_required
from .models.income_expense_item import IncomeExpenseItem
from .models.monthly_record import MonthlyRecord
from .models import db
from . import transactions_blueprint
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from flask_jwt_extended import jwt_required, get_jwt_identity


@transactions_blueprint.route('/api/v1/transactions/item/<int:item_id>', methods=['GET'])
@jwt_required()
def get_transaction_item(item_id):
    user_id = get_jwt_identity()

    # ユーザーIDとアイテムIDに基づいて入出金事項を取得
    item = IncomeExpenseItem.query.filter_by(id=item_id, user_id=user_id).first()

    # アイテムが存在しない場合のエラーレスポンス
    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404

    # アイテムデータのレスポンス
    item_data = {
        "id": item.id,
        "item_name": item.item_name,
        "item_type": item.item_type,
        "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # assuming created_at is a datetime field
        "updated_at": item.updated_at.strftime('%Y-%m-%d %H:%M:%S')   # assuming updated_at is a datetime field
    }

    return jsonify({"status": "success", "item": item_data}), 200


@transactions_blueprint.route('/api/v1/transactions/item', methods=['POST'])
@jwt_required()
def add_item():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    item_type = request.json.get('ItemType', None)
    item_name = request.json.get('ItemName', None)

    if not item_type or item_type not in ['income', 'expense']:
        return jsonify({"status": "error", "message": "Invalid or missing ItemType parameter"}), 400
    if not item_name:
        return jsonify({"status": "error", "message": "Missing ItemName parameter"}), 400

    user_id = get_jwt_identity()

    new_item = IncomeExpenseItem(user_id=user_id, item_name=item_name, item_type=item_type)
    
    new_item.created_by = user_id
    new_item.updated_by = user_id
    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"status": "success", "message": "Item added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "An error occurred: " + str(e)}), 500


@transactions_blueprint.route('/api/v1/transactions/item/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_transaction_item(item_id):
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    item_type = request.json.get('ItemType')
    item_name = request.json.get('ItemName')

    if not any([item_type, item_name]):
        return jsonify({"status": "error", "message": "Provide at least one parameter to update (ItemType or ItemName)"}), 400

    user_id = get_jwt_identity()

    item = IncomeExpenseItem.query.get(item_id)
    if not item:
        return jsonify({"status": "error", "message": "Item not found"}), 404
    if item.user_id != user_id:
        return jsonify({"status": "error", "message": "You are not authorized to update this item"}), 403

    if item_type:
        if item_type not in ['income', 'expense']:
            return jsonify({"status": "error", "message": "Invalid ItemType parameter"}), 400
        item.item_type = item_type

    if item_name:
        item.item_name = item_name

    item.updated_by = user_id  # Typo fix: update_by -> updated_by
    try:
        db.session.commit()
        return jsonify({"status": "success", "message": "Transaction item updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "An error occurred: " + str(e)}), 500
    

@transactions_blueprint.route('/api/v1/transactions/items', methods=['GET'])
@jwt_required()
def get_items():
    user_id = get_jwt_identity()

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
@jwt_required()
def add_monthly_transactions():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    # JSONリクエストから取引データを取得
    transactions = request.json.get('transactions')
    if not transactions:
        return jsonify({"status": "error", "message": "Missing transactions data"}), 400
    
    user_id = get_jwt_identity()
    new_records = []

    for transaction in transactions:
        month = transaction.get('Month')
        amount = transaction.get('Amount')
        item_name = transaction.get('ItemName')

        if not all([month, amount, item_name]):
            continue  # いずれかのキーが不足している場合はスキップ

        item = IncomeExpenseItem.query.filter_by(item_name=item_name, user_id=user_id).first()
        if not item:
            continue  # アイテムが見つからない場合はスキップ

        new_record = MonthlyRecord(
            user_id=user_id,
            income_expense_item_id=item.id,
            month=month,
            amount=amount
        )
        new_records.append(new_record)

    db.session.add_all(new_records)
    db.session.commit()

    return jsonify({"status": "success", "message": "Monthly transactions added successfully!"}), 201


@transactions_blueprint.route('/api/v1/transactions/monthly/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_monthly_transaction(transaction_id):
    user_id = get_jwt_identity()  # JWTからユーザーIDを取得
    record = MonthlyRecord.query.filter_by(id=transaction_id, user_id=user_id).first()

    if not record:
        return jsonify({"status": "error", "message": "Transaction not found"}), 404

    data = request.get_json()
    month = data.get("month")
    amount = data.get("amount")
    item_name = data.get("item_name")

    if item_name:
        item = IncomeExpenseItem.query.filter_by(item_name=item_name, user_id=user_id).first()
        if not item:
            return jsonify({"status": "error", "message": "Item not found"}), 404
        record.income_expense_item_id = item.id

    if month:
        record.month = month
    if amount:
        record.amount = amount

    db.session.commit


@transactions_blueprint.route('/api/v1/transactions/monthly', methods=['GET'])
@jwt_required()  # JWTトークンが有効かチェック
def get_monthly_transactions():
    month = request.args.get('month')  # クエリパラメータから月を取得
    user_id = get_jwt_identity()  # JWTからユーザーIDを取得

    try:
        if month:
            # 月が指定された場合、その月の入出金のみを取得
            transactions = MonthlyRecord.query.filter(and_(MonthlyRecord.user_id == user_id, MonthlyRecord.month == month)).options(joinedload(MonthlyRecord.income_expense_item)).all()
        else:
            # 月が指定されていない場合、全ての入出金を取得
            transactions = MonthlyRecord.query.filter_by(user_id=user_id).options(joinedload(MonthlyRecord.income_expense_item)).all()

        transactions_list = [{
            "id": transaction.id,
            "month": transaction.month,
            "amount": str(transaction.amount),
            "item_name": transaction.income_expense_item.item_name,
            "item_type": transaction.income_expense_item.item_type
        } for transaction in transactions]

        return jsonify({
            "success": True,
            "transactions": transactions_list
        }), 200

    except Exception as e:
        # エラーが発生した場合
        return jsonify({
            "success": False,
            "errors": [str(e)]
        }), 500