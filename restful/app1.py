from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
from flask import Flask, request, jsonify
import random

app = Flask(__name__)
api = Api(app=app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


api.add_resource(TodoSimple, '/<string:todo_id>')


"""
Request Parsing
"""
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)
parser.add_argument('rate', type=int, help='Rate cannot be converted')

parser.add_argument('name1', type=str, action='append')
# Look only in the POST body
parser.add_argument('name', type=int, location='form')
# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')
# From the request headers
parser.add_argument('User-Agent', type=str, location='headers')
# From http cookies
parser.add_argument('session_id', type=str, location='cookies')
# From file uploads
# parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

parser.add_argument('text', location=['headers', 'values'])
# args = parser.parse_args()

resource_fields = {
    'name': fields.String(default='ash'),
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
}


class Todo(Resource):
    @marshal_with(resource_fields, envelope='data')
    def get(self, **kwargs):
        return self.db_get_todo()

    def db_get_todo(self):
        return {
            "name": 'ash',
            'address': '2018 01 11'
            # 'date_updated': datetime.utctimetuple()
        }


"""
自定义字段&多个值
有时候你有你自己定义格式的需求。你可以继承 fields.Raw 类并且实现格式化函数。
当一个属性存储多条信息的时候是特别有用的。例如，一个位域（bit-field）各位代表不同的值。
你可以使用 fields 复用一个单一的属性到多个输出值（一个属性在不同情况下输出不同的结果）。

这个例子假设在 flags 属性的第一位标志着一个“正常”或者“迫切”项，第二位标志着“读”与“未读”。
这些项可能很容易存储在一个位字段，但是可读性不高。转换它们使得具有良好的可读性是很容易的。
"""


class UrgentItem(fields.Raw):
    def format(self, value):
        return 'Urgent' if value & 0x01 else 'Normal'


class UnreadItem(fields.Raw):
    def format(self, value):
        return 'Unread' if value & 0x02 else 'Read'


fields1 = {
    'name': fields.String(default='ash'),
    'priority': UrgentItem(attribute='flags'),
    'status': UnreadItem(attribute='flags'),
}


class Todo1(Resource):
    @marshal_with(fields1, envelope='data')
    def get(self, **kwargs):
        return {'priority': '123'}


"""
Url & 其它具体字段
Flask-RESTful 包含一个特别的字段，fields.Url，即为所请求的资源合成一个 uri。
这也是一个好示例，它展示了如何添加并不真正在你的数据对象中存在的数据到你的响应中。
"""


class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()


fields2 = {
    'name': fields.String(default='ash'),
    # todo_resource is the endpoint name when you called api.add_resource()
    'uri': fields.Url('todo1', absolute=True),
    'https_uri': fields.Url('todo', absolute=True, scheme='https'),
    'random': RandomNumber
}


class Todo2(Resource):
    @marshal_with(fields2, envelope='data')
    def get(self, **kwargs):
        return {'uri': 'None'}


"""
复杂结构¶
你可以有一个扁平的结构，marshal_with 将会把它转变为一个嵌套结构
"""


class Todo3(Resource):
    def get(self):
        resource_fields = {'name': fields.String}
        resource_fields['address'] = {}
        resource_fields['address']['line 1'] = fields.String(attribute='addr1')
        resource_fields['address']['line 2'] = fields.String(attribute='addr2')
        resource_fields['address']['city'] = fields.String
        resource_fields['address']['state'] = fields.String
        resource_fields['address']['zip'] = fields.String

        data = {'name': 'bob', 'addr1': '123 fake street', 'addr2': '', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
        return jsonify(marshal(data, resource_fields))
        

api.add_resource(Todo, '/todo')
api.add_resource(Todo1, '/todo1')
api.add_resource(Todo2, '/todo2')
api.add_resource(Todo3, '/todo3')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)
