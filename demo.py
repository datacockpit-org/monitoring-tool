from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import yaml
from random import randint
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Configure the SQLite database
# CHANGE THE FOLLOWING TO YOUR SQLITE DB PATH:
database_path = '/Users/suryashekharchakraborty/mydatabase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path

if database_path == '/Users/YOURUSERNAME/mydatabase.db':
    print("Did you remember to change the database path?")

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

class record_metrics(db.Model):
    db_name = db.Column(db.String(100), primary_key=True)
    table_name = db.Column(db.String(100), primary_key=True)
    primary_key = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    uniqueness = db.Column(db.Float)
    completeness = db.Column(db.Float)
    correctness = db.Column(db.Float)
    freshness = db.Column(db.Float)
    overall = db.Column(db.Float)

class attribute_metrics(db.Model):
    db_name = db.Column(db.String(100), primary_key=True)
    table_name = db.Column(db.String(100), primary_key=True)
    attribute_name = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    uniqueness = db.Column(db.Float)
    completeness = db.Column(db.Float)
    correctness = db.Column(db.Float)
    overall = db.Column(db.Float)


class dcp_dataset_usage(db.Model):
    database = db.Column(db.String(100), primary_key=True)
    dataset = db.Column(db.String(100), primary_key=True)
    query_count = db.Column(db.Integer)
    unique_user_count = db.Column(db.Integer)
    dataset_usage_frequency_score = db.Column(db.Float)
    no_of_unique_users_score = db.Column(db.Float)
    overall_dataset_usage_score = db.Column(db.Float)


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
    for du in dcp_du[:20]:
        rows.append({
            "name": f"{du.database}.{du.dataset}",
            "is_leaf": True,
            "usage_insights": {
                "query_count": {
                    "name": "query_count",
                    "unit": "",
                    "description": "Count of queries",
                    "value": du.query_count
                },
                "unique_user_count": {
                    "name": "unique_user_count",
                    "unit": "",
                    "description": "Count of unique users",
                    "value": du.unique_user_count
                },
                "dataset_usage_frequency_score": {
                    "name": "dataset_usage_frequency_score",
                    "unit": "",
                    "description": "Dataset usage frequency score",
                    "value": du.dataset_usage_frequency_score
                },
                "no_of_unique_users_score": {
                    "name": "no_of_unique_users_score",
                    "unit": "",
                    "description": "Unique users score",
                    "value": du.no_of_unique_users_score
                },
                "overall_dataset_usage_score": {
                    "name": "overall_dataset_usage_score",
                    "unit": "",
                    "description": "Overall dataset usage score",
                    "value": du.overall_dataset_usage_score
                }
            },
            "quality_insights": {
                "correctness": {
                    "name": "Correctness",
                    "unit": "%",
                    "description": "Correctness",
                    "value": randint(70, 100)
                },
                "completeness": {
                    "name": "Completeness",
                    "unit": "%",
                    "description": "Completeness",
                    "value": randint(70, 100)
                }
            }
        })
    result["children"] = rows
    return jsonify(result)

# For the sake of the demo, we are combining the output of handcrafted data for quality
# and DBDEO data for usage.
@app.route('/get_subset')
@cross_origin()
def get_subset():
    dcp_du = dcp_dataset_usage.query.all()
    att_mets = attribute_metrics.query.all()
    print(att_mets[0])
    print("Number of responses: ", len(dcp_du))
    result = {"name": "dcp_dataset_usage"}
    rows = []
    for i in range(20):
        du, am = dcp_du[i%len(dcp_du)], att_mets[i%len(att_mets)] # to prevent overflow
        rows.append({
            "name": f"{du.database}.{du.dataset}",
            "is_leaf": True,
            "usage_insights": {
                "query_count": {
                    "name": "query_count",
                    "unit": "",
                    "description": "Count of queries",
                    "value": du.query_count
                },
                "unique_user_count": {
                    "name": "unique_user_count",
                    "unit": "",
                    "description": "Count of unique users",
                    "value": du.unique_user_count
                },
                "dataset_usage_frequency_score": {
                    "name": "dataset_usage_frequency_score",
                    "unit": "",
                    "description": "Dataset usage frequency score",
                    "value": du.dataset_usage_frequency_score
                },
                "no_of_unique_users_score": {
                    "name": "no_of_unique_users_score",
                    "unit": "",
                    "description": "Unique users score",
                    "value": du.no_of_unique_users_score
                },
                "overall_dataset_usage_score": {
                    "name": "overall_dataset_usage_score",
                    "unit": "",
                    "description": "Overall dataset usage score",
                    "value": du.overall_dataset_usage_score
                }
            },
            "quality_insights": {
                "correctness": {
                    "name": "Correctness",
                    "unit": "%",
                    "description": "Correctness",
                    "value": am.correctness,
                },
                "completeness": {
                    "name": "Completeness",
                    "unit": "%",
                    "description": "Completeness",
                    "value": am.completeness,
                },
                "uniqueness": {
                    "name": "Uniqueness",
                    "unit": "%",
                    "description": "Uniqueness",
                    "value": am.uniqueness,
                },
                "overall": {
                    "name": "Overall",
                    "unit": "%",
                    "description": "Overall",
                    "value": am.overall,
                }
            }
        })
    result["children"] = rows
    return jsonify(result)




# For the sake of the demo, we are combining the output of handcrafted data for quality
# and DBDEO data for usage.
@app.route('/get_all')
@cross_origin()
def get_all():
    dcp_du = dcp_dataset_usage.query.all()
    att_mets = attribute_metrics.query.all()
    print("Number of responses: ", len(dcp_du))
    result = {"name": "dcp_dataset_usage"}
    rows = []
    for i in range(len(dcp_du)-1):
        du, am = dcp_du[i%len(dcp_du)], att_mets[i%len(att_mets)] # to prevent overflow
        rows.append({
            "name": f"{du.database}.{du.dataset}",
            "is_leaf": True,
            "usage_insights": {
                "query_count": {
                    "name": "query_count",
                    "unit": "",
                    "description": "Count of queries",
                    "value": du.query_count
                },
                "unique_user_count": {
                    "name": "unique_user_count",
                    "unit": "",
                    "description": "Count of unique users",
                    "value": du.unique_user_count
                },
                "dataset_usage_frequency_score": {
                    "name": "dataset_usage_frequency_score",
                    "unit": "",
                    "description": "Dataset usage frequency score",
                    "value": du.dataset_usage_frequency_score
                },
                "no_of_unique_users_score": {
                    "name": "no_of_unique_users_score",
                    "unit": "",
                    "description": "Unique users score",
                    "value": du.no_of_unique_users_score
                },
                "overall_dataset_usage_score": {
                    "name": "overall_dataset_usage_score",
                    "unit": "",
                    "description": "Overall dataset usage score",
                    "value": du.overall_dataset_usage_score
                }
            },
            "quality_insights": {
                "correctness": {
                    "name": "Correctness",
                    "unit": "%",
                    "description": "Correctness",
                    "value": am.correctness,
                },
                "completeness": {
                    "name": "Completeness",
                    "unit": "%",
                    "description": "Completeness",
                    "value": am.completeness,
                },
                "uniqueness": {
                    "name": "Uniqueness",
                    "unit": "%",
                    "description": "Uniqueness",
                    "value": am.uniqueness,
                },
                "overall": {
                    "name": "Overall",
                    "unit": "%",
                    "description": "Overall",
                    "value": am.overall,
                }
            }
        })
    result["children"] = rows
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)

# Then, in a new terminal from the monitoring-tool directory,
# run: curl -o data/attribute_tree.json http://127.0.0.1:5000/get_all
