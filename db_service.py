from flask import Flask, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

import psycopg2
import yaml
from random import randint
from jinja2 import TemplateNotFound

with open('credentials.yml', 'r') as f:
    credentials = yaml.safe_load(f)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# e.g. postgres://surya:1234@localhost:5432/surya
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"{credentials['database']['type']}://{credentials['database']['user']}:" + \
    f"{credentials['database']['password']}@{credentials['database']['host']}" + \
    f":{credentials['database']['port']}/{credentials['database']['name']}"

db = SQLAlchemy(app)

class Users(db.Model):  # this name has to be the same as DB name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class dcp_dataset_usage(db.Model):
    database                        = db.Column(db.String(100), primary_key=True)
    dataset                         = db.Column(db.String(100), primary_key=True)
    query_count                     = db.Column(db.Integer)
    unique_user_count               = db.Column(db.Integer)
    dataset_usage_frequency_score   = db.Column(db.Float)
    no_of_unique_users_score        = db.Column(db.Float)
    overall_dataset_usage_score     = db.Column(db.Float)


@app.route('/users')
def get_users():
    users = Users.query.all()

    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

    return jsonify(result)



@app.route('/dcp_dataset_usage')
@cross_origin()
def get_dcp_dataset_usages():
    dcp_du = dcp_dataset_usage.query.all()
    print("Number of responses: ", len(dcp_du))
    result = {"name": "dcp_dataset_usage"}
    rows = []
    for du in dcp_du[:10]:
        rows.append({
            "name": f"{du.database}.{du.dataset}",
            "is_leaf": True,
            "usage_insights": {
                "query_count":{
                    "name": "query_count",
                    "unit": "",
                    "description": "Count of queries",
                    "value": du.query_count
                },
                "unique_user_count":{
                    "name": "unique_user_count",
                    "unit": "",
                    "description": "Count of unique users",
                    "value": du.unique_user_count
                },
                "dataset_usage_frequency_score":{
                    "name": "dataset_usage_frequency_score",
                    "unit": "",
                    "description": "Dataset usage frequency score",
                    "value": du.dataset_usage_frequency_score
                },
                "no_of_unique_users_score":{
                    "name": "no_of_unique_users_score",
                    "unit": "",
                    "description": "Unique users score",
                    "value": du.no_of_unique_users_score
                },
                "overall_dataset_usage_score":{
                    "name": "overall_dataset_usage_score",
                    "unit": "",
                    "description": "Overall dataset usage score",
                    "value": du.overall_dataset_usage_score
                }
            },
            "quality_insights": {
                "correctness":{
                    "name": "Correctness",
                    "unit": "%",
                    "description": "Correctness",
                    "value": randint(70, 100)
                },
                "completeness":{
                    "name": "Completeness",
                    "unit": "%",
                    "description": "Completeness",
                    "value": randint(70, 100)
                }
            }
        })
    result["children"] = rows
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
