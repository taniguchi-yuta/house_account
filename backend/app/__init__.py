from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from .users.models.user import User
from .transactions.models import db
from .users import users_blueprint
from .transactions import transactions_blueprint
from flask_cors import CORS

# dotenvの設定を読み込む
load_dotenv("../.env.local")

app = Flask(__name__)
# allowed_origins = os.environ.get('ALLOWED_ORIGINS').split(',')
CORS(app, supports_credentials=True)
api = Api(app)

# 本番環境では安全なキーを使用してください
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db:3306/house_account_local'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 通常は不要なのでFalseにしておきます。

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_default_key')

#users/__init__.pyで定義したBlueprintをセット
app.register_blueprint(users_blueprint)
#transactions/__init__.pyで定義したBlueprintをセット
app.register_blueprint(transactions_blueprint)

# modelsで作成したdbインスタンスをインポート
db.init_app(app)

# Migrateのインスタンスを作成
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))