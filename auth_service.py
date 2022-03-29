from functools import wraps
import traceback
from flask import request
import jwt
import config
import es_service
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

def authenticate(object):
    '''
    Token authenticator
    '''
    @wraps(object)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            response = {"success": False, "message":"Token missing"}
            return response
        try:
            data = jwt.decode(token.split(" ")[1], config.config['secret_key'], algorithms=config.config['algorithms'])
        except:
            traceback.print_exc()
            response = {"success": False, "message":"Invalid token"}
            return response
        return  object(*args, **kwargs)
    return decorated

def token_validator(userId, password):
    '''
    Validate the token against request token
    '''
    if not userId or not password:
        response = {"success": False, "message":"UserID / Password missing."}, 400
        return response
    else:
        user_query = es_service.build_query(timerange = False, user_id = userId)
        user_data, count = es_service.get_data("user_details",user_query)
        if not user_data:
            response = {"success":False, "message":"Please register user."}
        else:
            if check_password_hash(user_data[0]['password'], password):
                token = jwt.encode({
                                    'user_id': user_data[0]['user_id'],
                                    'exp' : datetime.utcnow() + timedelta(minutes = 60)
                                    }, config.config['secret_key'])
                response = {"success":True, "message":"Login successful!", "token":token}
            else:
                response = {"success":False, "message":"Invalid password for the user ID."}

    return response

def generate_password(password):
    return generate_password_hash(password)

def create_audit_user(userId, password):
    if not userId or not password:
        response = {"success": False, "message":"UserID / Password missing."}, 400
        return response
    es_obj = {
        'user_id' : userId,
        'password' : generate_password(password),
    }
    response = es_service.index_data("user_details", es_obj)
    return response

def add_audit_log(user_id, action, action_doc, timestamp):
    if not (action and user_id and action_doc):
        response = {"success":False, "message":"Field missing"}, 400
        return response

    es_obj = {
        'date' : timestamp,
        'action' : action,
        'action_document' : action_doc,
        'user_id' : user_id
    }
    response = es_service.index_data("audit_logs",es_obj)
    return response

def get_audit_log(userId, action):
    query = es_service.build_query(timerange = True, user_id = userId, action = action)
    result, count = es_service.get_data("audit_logs", query)
    return result, count