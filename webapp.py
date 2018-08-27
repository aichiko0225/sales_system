import logging
from flask import Flask, render_template, make_response
from routes.index import main
from routes import allow_cross_domain
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
CORS(app, supports_credentials=True)


# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = 'random string'

app.register_blueprint(main, url_prefix='/account')


@app.route('/')
# @allow_cross_domain
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
