from flask import jsonify, request
from flask_login import current_user, login_required
from .models.income_expense_item import IncomeExpenseItem
from .models import db
from . import transactions_blueprint

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