
import flask
from flask import  Flask, jsonify, request
import werkzeug
# import flask_restplus
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
werkzeug.cached_property = werkzeug.utils.cached_property
import collections
from collections import abc
collections.MutableMapping = abc.MutableMapping
from flask_restplus import Resource, Api, reqparse , abort
application = app = Flask(__name__)
api= Api(app)
todos= {
    1:{'name': 'Amber Heard', 'score': 870},
    2:{'name': 'Win Ryder', 'score': 880},
    3:{'name': 'Johnny Deep', 'score': 900}
}
#declare argument
task_post_args= reqparse.RequestParser()
task_post_args.add_argument("name", type= str, help= "Name is required", required= True )
task_post_args.add_argument('score', type= int, help= 'Score is required', required= True )

#get all value of list
class ToDolist(Resource):
    def get(self):
        return todos
class ToDo(Resource):
    def get(self, todo_id):
        return  todos[todo_id]
    def post(self, todo_id):
        args= task_post_args.parse_args()
        if todo_id in todos:
            abort(409, "userID already taken")
        #add new id into data
        todos[todo_id]= {"name": args["name"], "score": args["score"]}
        return todos[todo_id]

api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDolist, '/todos')

if __name__== '__main__':
    app.run(debug=True)