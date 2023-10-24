from flask import jsonify, request
from ..transactions.models import db
from .models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_blueprint
from flask_login import login_user, logout_user, current_user


@users_blueprint.route('/api/v1/users/check_auth', methods=['GET'])
def check_auth():
    if current_user.is_authenticated:
        return jsonify({"status": "success", "logged_in": True, "user": current_user.email_address}), 200
    else:
        return jsonify({"status": "error", "logged_in": False, "message": "User not logged in"}), 401


@users_blueprint.route('/api/v1/users/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    email = request.json.get('emailAddress', None)
    password = request.json.get('password', None)
    name = request.json.get('name', None)

    if not email:
        return jsonify({"status": "error", "message": "Missing emailAddress parameter"}), 400
    if not password:
        return jsonify({"status": "error", "message": "Missing password parameter"}), 400

    user = User.query.filter_by(email_address=email).first()
    if user:
        return jsonify({"status": "error", "message": "User already exists"}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(email_address=email, hashed_password=hashed_password, name=name)

    db.session.add(new_user)
    db.session.flush()  # This will generate the new user's ID without committing the transaction
    new_user.created_by = new_user.id
    new_user.updated_by = new_user.id
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered"}), 201


@users_blueprint.route('/api/v1/users/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    email = request.json.get('emailAddress', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"status": "error", "message": "Missing emailAddress parameter"}), 400
    if not password:
        return jsonify({"status": "error", "message": "Missing password parameter"}), 400

    user = User.query.filter_by(email_address=email).first()
    if not user:
        return jsonify({"status": "error", "message": "User does not exist"}), 401

    # 保存されているハッシュ化されたパスワードと入力されたパスワードを確認
    if check_password_hash(user.hashed_password, password):
        login_user(user)
        # この部分では、例えばJWTなどを使用してトークンを返すなど、ログインに成功した後の処理を実装できます。
        return jsonify({"status": "success", "message": "Login successful"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@users_blueprint.route('/api/v1/users/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200


@users_blueprint.route('/api/v1/users/update', methods=['PUT'])
def update_user_info():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400

    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    email = request.json.get('emailAddress', None)
    password = request.json.get('password', None)
    name = request.json.get('name', None)

    if email:
        existing_user = User.query.filter_by(email_address=email).first()
        if existing_user and existing_user.id != current_user.id:
            return jsonify({"status": "error", "message": "Email address already in use by another user"}), 400
        current_user.email_address = email

    if password:
        hashed_password = generate_password_hash(password, method='sha256')
        current_user.hashed_password = hashed_password

    if name:
        current_user.name = name

    current_user.upated_by = current_user.id
    db.session.commit()

    return jsonify({"status": "success", "message": "User information updated successfully"}), 200