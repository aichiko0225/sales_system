from flask import Blueprint
# from flask_restful import Resource, Api
# from webapp import app

hello = Blueprint('hello', __name__)
# api = Api(app)

"""
这个文件主要介绍flask restful， 简单介绍学习一下
"""


@hello.route('/', methods=["POST"])
def index():
    return 'hello world'


# api.add_resource(HelloWorld, '/a')
