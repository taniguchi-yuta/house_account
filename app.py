from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # 本番環境では安全なキーを使用してください
jwt = JWTManager(app)

# ルートの設定
@app.route('/')
def index():
    return "House Account App API"

# これ以降、APIリソースやモデルなどのセットアップを行います。
