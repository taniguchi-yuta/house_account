# ベースとなるイメージを指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# requirements.txtをコンテナにコピー
COPY ./backend/requirements.txt ./requirements.txt

# ライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# .env ファイルをコピー（ルートディレクトリから）
COPY .env.development ./
COPY .env.production ./

# アプリケーションのソースをコピー
COPY ./backend ./

# Flaskの実行
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
