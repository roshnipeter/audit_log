from datetime import datetime, timedelta
from elasticsearch import helpers, Elasticsearch
import config

to_date = datetime.now()
from_date = to_date - timedelta(days=10)

es = Elasticsearch(config.config['es_host'])

def build_query(timerange = True, **kwargs):
    filter = []
    query = {
        "query": {
            "bool": {
            "must": [],
            "filter": [
                {
                    "match_all": {}
                }
            ],
            "should": [],
            "must_not": []
            }   
        }
    }
    for key, value in kwargs.items():
        if value:
            filter.append({
                "match_phrase": {
                    "{}.keyword".format(key): value
                }
        })
    
    if timerange:
        filter.append({
            "range": {
                "date": {
                        "gte": from_date.strftime("%Y-%m-%d"),
                        "lte": to_date.strftime("%Y-%m-%d"),
                        "format": "strict_date_optional_time"
                    }
                }
            })

    query['query']['bool']['filter'].extend(filter) if filter else None
    print(query)
    return query

def get_data(index, query):
    '''
    Returns the data from the given ES index
    params: 
        index - es index name
        query - query for ES search
    '''
    total_count = 0
    result_list = []
    for es_doc in helpers.scan(client=es, query=query, index=index, size=2000, scroll="5s"):
        result_list.append(es_doc["_source"])
        total_count += 1
    return (result_list, total_count)

def index_data(index, es_obj):
    '''
    Indexes the data to given ES index
    params: 
        index - es index name
        es_obj - document for ES
    '''
    try:
        es.index(index = index, body = es_obj)
        response = {"success":True, "message":"Audit added successfully!"}
    except:
        response = {"success":False, "message":"Audit not added."} 
    return response 
