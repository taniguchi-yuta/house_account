# users/__init__.py

from .models import user
from flask import Blueprint

# "users" Blueprintの定義。これを使ってルーティングをグループ化します。
users_blueprint = Blueprint('users', __name__)

# ここでmodelsやroutesなど、usersパッケージ内の他のモジュールをインポートします。
# from . import routes, utils
