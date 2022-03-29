from distutils.command.config import config
from http.client import REQUEST_TIMEOUT
import os
import traceback
import flask
from flask import request, jsonify, abort
from elasticsearch import Elasticsearch, helpers
from datetime import datetime, timedelta
import jwt
from sqlalchemy import true
import yaml
import query_builder
from  werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

es = Elasticsearch("http://localhost:9200")

config_file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_file_path) as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = config['secret_key']

def get_data(index, query):
    total_count = 0
    result_list = []
    for es_doc in helpers.scan(client=es, query=query, index=index, size=2000, scroll="5s"):
        result_list.append(es_doc["_source"])
        total_count += 1
    response = {'success': True, 'data':result_list, 'count':total_count} if result_list else {'success': False, 'data':result_list, 'count':total_count}
    return response


def authenticate(token):
    try:
        user_data = jwt.decode(token, app.config['SECRET_KEY'],  algorithms="HS256")
        return True
    except:
        return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


@app.route('/audit',methods = ['POST'])
def add_audit():
    token = request.headers.get('x-access-token')
    if not token:
        response = {"success": False, "message":"Token missing"}
        return response
    
    if authenticate(token):
        data = request.get_json()
        user_id = data.get('id')
        action = data.get('action')
        timestamp = datetime.now()
        action_doc = data.get('action_doc')

        if not (action and user_id and action_doc):
            response = {"success":False, "message":"Field missing"}
            return response

        es_obj = {
            'date' : timestamp,
            'action' : action,
            'action_document' : action_doc,
            'user_id' : user_id
        }
        try:
            es.index(index = 'audit_logs', body = es_obj)
            response = {"success":True, "message":"Audit added successfully!"}
        except:
            response = {"success":False, "message":"Audit not added."}  
    else:
        response = {"success": False, "message":"Invalid token."}
    return response


@app.route('/audit',methods = ['GET'])
def get_audit():
    userId = request.args.get('id')
    action = request.args.get('action')
    token = request.headers.get('x-access-token')
    if not token:
        response = {"success": False, "message":"Token missing."}, 404
        return response
    if authenticate(token):
        query = query_builder.build_query(timerange = True, user_id = userId, action = action)
        response = get_data("audit_logs", query)
    else:
        response = {"success": False, "message":"Invalid token."}, 401
    return response


@app.route('/user',methods = ['POST'])
def create_user():
    data = request.get_json()
    userId = data.get('username')
    password = data.get('password')
    if not userId or not password:
        response = {"success": False, "message":"UserID / Password missing."}, 400
        return response
    es_obj = {
        'user_id' : userId,
        'password' : generate_password_hash(password),
    }
    try:
        es.index(index = 'user_details', body = es_obj)
        response = {"success":True, "message":"User created successfully!"}, 200
    except:
        response = {"success":False, "message":"User not created."}, 401
    return response


@app.route('/login',methods = ['POST'])
def login_user():
    data = request.get_json()
    userId = data.get('username')
    password = data.get('password')
    if userId is None or password is None:
        response = {"success": False, "message":"UserID / Password missing."}, 400
        return response
    else:
        user_query = query_builder.build_query(timerange = False, user_id = userId)
        user_data = get_data("user_details",user_query)
        if not user_data:
            response = {"success":False, "message":"Please register user."}
        else:
            if check_password_hash(user_data['data'][0]['password'], password):
                token = jwt.encode({
                                    'user_id': user_data['data'][0]['user_id'],
                                    'exp' : datetime.utcnow() + timedelta(minutes = 60)
                                    }, app.config['SECRET_KEY'])
                response = {"success":True, "message":"Login successful!", "token":token}, 200
            else:
                response = {"success":False, "message":"Invalid password for the user ID."}, 401
    return response
    
    
app.run(port=3000)