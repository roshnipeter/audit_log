from datetime import datetime, timedelta

to_date = datetime.now()
from_date = to_date - timedelta(days=10)

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
