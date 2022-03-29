import flask
from flask import request
from datetime import datetime
from auth_service import authenticate, token_validator, create_audit_user, add_audit_log, get_audit_log

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/audit',methods = ['POST'])
@authenticate
def add_audit():
    '''
    To add any log to ES.
    '''
    data = request.get_json()
    user_id = data.get('id')
    action = data.get('action')
    timestamp = datetime.now()
    action_doc = data.get('action_doc')

    response = add_audit_log(user_id, action, action_doc, timestamp)

    if response['success']:
        return response, 200 
    else:
        return response, 401


@app.route('/audit',methods = ['GET'])
@authenticate
def get_audit():
    '''
    To retrieve data from ES
    '''
    userId = request.args.get('id')
    action = request.args.get('action')
    result, count = get_audit_log(userId, action)
    if result:
        response = {"success":True, "data":result, "count":count}, 200
    else:
        response = {"success":False, "data":result, "count":count}, 400
    return response


@app.route('/user',methods = ['POST'])
def create_user():
    '''
    Creating a user.
    '''
    data = request.get_json()
    userId = data.get('username')
    password = data.get('password')
    response = create_audit_user(userId, password)
    if response['success']:
        return response, 200 
    else:
        return response, 401


@app.route('/login',methods = ['POST'])
def login_user():
    '''
    User login. On successful login, a token is generated that is valid for 60 minutes(hardcoded)
    '''
    data = request.get_json()
    userId = data.get('username')
    password = data.get('password')
    response = token_validator(userId, password)
    if response['success']:
        return response, 200 
    else:
        return response, 401
    
    
if __name__ == "__main__":
    app.run(port=3000)