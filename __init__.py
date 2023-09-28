from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

# dotenvの設定を読み込む
load_dotenv(".env.local")

app = Flask(__name__)
api = Api(app)

# 本番環境では安全なキーを使用してください
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db:3306/house_account_local'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 通常は不要なのでFalseにしておきます。

# modelsで作成したdbインスタンスをインポート
from .models import db
db.init_app(app)

# Migrateのインスタンスを作成
migrate = Migrate(app, db)

from . import models
