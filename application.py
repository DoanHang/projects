# import flask_restplus
import flask.scaffold
import werkzeug
from flask import Flask

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
werkzeug.cached_property = werkzeug.utils.cached_property
import collections
from collections import abc

collections.MutableMapping = abc.MutableMapping
from flask_restplus import Resource, Api, reqparse, abort
import pandas as pd
import boto3
bucket = "elasticbeanstalk-us-east-1-766718850528"
file_name = "sample.csv"
s3 = boto3.client('s3')
obj = s3.get_object(Bucket= bucket, Key= file_name)
# get object and file (key) from bucket
initial_df = pd.read_csv(obj['Body'])
def read_file(initial_df):
    """
    used to read input data file with format CSV
    return:
    data with format dict
    """
    # df = pd.read_csv("F:\\EXTRA_PROJECT\\flask_rest_api_database\\sample.csv")
    df= initial_df
    print(df.shape[0])
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns='Unnamed: 0')
    data_dict = df.to_dict('index')
    return data_dict

application = app = Flask(__name__)
api = Api(app)
todos = read_file()
# todos= {
#     1:{'name': 'Amber Heard', 'score': 870},
#     2:{'name': 'Win Ryder', 'score': 880},
#     3:{'name': 'Johnny Deep', 'score': 900}
# }
# declare argument
task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type=str, help="Name is required", required=True)
task_post_args.add_argument('score', type=int, help='Score is required', required=True)


# get all value of list
class ToDolist(Resource):
    def get(self):
        return todos


class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        args = task_post_args.parse_args()
        if todo_id in todos:
            abort(409, "userID already taken")
        # add new id into data
        todos[todo_id] = {"name": args["name"], "score": args["score"]}
        return todos[todo_id]


api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDolist, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
