from .__init__ import app

# ルートの設定
@app.route('/')
def index():
    return "House Account App API"

