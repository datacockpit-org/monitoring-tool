from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import psycopg2
import yaml

with open('credentials.yml', 'r') as f:
    credentials = yaml.safe_load(f)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{credentials['database']['user']}:" + \
    f"{credentials['database']['password']}@{credentials['database']['host']}" + \
    f":{credentials['database']['port']}/{credentials['database']['name']}"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


@app.route('/users')
def get_users():
    users = User.query.all()

    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
