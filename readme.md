# Requirements
## Audit Log API
 1. Create Audit Log
 2. Querry Audit Log
 3. Authentication

Write Intensive 


# AUDIT LOG SYSTEM

## This service is used to store and retrieve audit logs via HTTP requests. There are 2 methods - POST to send an audit log, GET to receive data as per filters applied if any. This is a write intensive function.

# Technologies used

## Python3 - Flask to render APIs
## Elasticsearch to store and retrieve data
## Kibana for visualising data

# Table of Contents

## api.py - Contains all the code. There are 2 APIs defined - GET(/audit) and POST(/audit)

## Structure of an ES document would be:
<!-- {
        'date' : timestamp, the date as of now.
        'action' : action, This field could be any action item the user does.
        'action_document' : action_doc, This is preferably a json, that is specific to the action item.
        'user_id' : user_id, A unique identifier for the user.
} -->

## The GET method retrieves info from ES. Can filter results by giving parameters - id(user_id), action, startDate, endDate(both  dates in 'MM-DD-YYYY format)

## The post method indexes data to ES.



token is provided at time of user creation

To implement - check the duplication of audit
Token is presently valid for 60 mins, can change
