# AUDIT LOG SYSTEM

This service is used to store and retrieve audit logs via HTTP requests. There are 2 methods - POST to send an audit log, GET to receive data as per filters applied if any. This is a write intensive function.

# Technologies used

1. Python3 - Flask to render APIs
2. Elasticsearch to store and retrieve data
3. Kibana for visualising data
4. JWT for authentication

# Table of Contents

1. audit_logger.py - Contains all the code
2. config.yaml - Contains all config information. Can be extended as per requirement.
3. query_builder.py - Contains the query building function for ES functionalities. Future scope is to extend this file to contain   all ES related activites.

# Functionalities

- The GET method "/audit" retrieves info from ES. Can filter results by giving parameters - id(user_id), action,

- The POST method "/audit" indexes data to ES. There are 4 fields in the ES document

1. date - present time
2. action - corresponding action verb
3. action_document - document w.r.t the action verb. This can be any data structure.
4. user_id - ID of the user who performs the action

Structure of an ES document would be:
```
{
        'date' : timestamp, the date as of now.
        'action' : action, This field could be any action item the user does.
        'action_document' : action_doc, This is preferably a json, that is specific to the action item.
        'user_id' : user_id, A unique identifier for the user.
}
```
- The POST method "/user" is to create a new user. 

- The POST method "/login" is used for user login. Upon successful login, token is generated, which is validated against for GET and POST **/audit** methods.

# How to run the program?
command to execute is **python audit_logger.py** The platform supports I've used are:
1. ElasticSearch - 7.10.2-SNAPSHOT
2. Kibana - 7.10.2
3. Postman - 9.15.6
