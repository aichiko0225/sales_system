from flask import Blueprint, jsonify, render_template, request, Response
from routes import allow_cross_domain
from models import Base
from sqlalchemy import Column, Integer, String
from routes import session
from utils import log
from models import ResponseModel

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
# 第二个参数是套路
main = Blueprint('account', __name__)


class Auth_User(Base):
    """
    定义Auth_User对象:
    """
    # 表的名字:
    __tablename__ = "auth_user"

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=30), unique=True)
    password = Column(String(length=128))

    @classmethod
    def find(cls, username: str, password: str):

        # session.query(Auth_User)
        return {
            'username': username,
            'user_id': 1000
        }


@main.route('/login', methods=["POST"])
def index():
    username = request.form.get('username')
    password = request.form.get('password')
    log(request.form)
    if username is None:
        response = ResponseModel(code=1, message='用户名不正确')
        return jsonify(response.__dict__)
    else:
        if len(username) > 0 and len(password) > 5:
            data = Auth_User.find(username=username, password=password)
            response = ResponseModel(code=0, message='登录成功', data=data)
            return jsonify(response.__dict__)
        else:
            response = ResponseModel(code=1, message='用户名不正确')
            return jsonify(response.__dict__)

