from flask import Flask,request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


users = {}

class User(Resource):
    def get(self, user_id):
        return {user_id: users[user_id]}

    def put(self, user_id):
        users[user_id] = request.form['data']
        return {user_id: users[user_id]}

api.add_resource(User, '/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
