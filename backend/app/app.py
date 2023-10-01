from .__init__ import app
from flask import jsonify, request
from .transactions.models import db
from .users.models.user import User
from werkzeug.security import generate_password_hash

# ルートの設定
@app.route('/')
def index():
    return "House Account App API"

@app.route('/api/v1/users/register', methods=['POST'])
def register():
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
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered"}), 201
