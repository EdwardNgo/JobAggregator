import logging
from elasticsearch import Elasticsearch
from mongo_helper import *
import requests
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def create_index(es_object, index_name,properties):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings":  {
                "dynamic": "strict",
                "properties":properties
            }
        
    }
    print(settings)
    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            print('hi')
            es_object.indices.create(index=index_name, body=settings)
            print('Created Index')
            created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def store_record(elastic_object, index_name,record):
    try:
        outcome = elastic_object.index(index=index_name, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def search_record(index_name,query):
    url = f'http://localhost:9200/{index_name}/_search?q={query}'
    res = requests.get(url)
    search_res = []
    try:
        hits = res.json()['hits']['hits']
        for hit in hits:
            print(hit)
            search_res.append(hit['_source'])
    except:
        print("Not found any value match your search")
    return search_res
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    # job = Job()
    # jobData = job.getJobData('site_job')
    # properties = {"title": {"type": "text"},"city": {"type": "text"},"url": {"type": "text"},"img": {"type": "text"},"salary": {"type": "text"},"update_time": {"type": "text"},"company": {"type": "text"}}
    # es = connect_elasticsearch() 

    # # create_index(es,'site_jobs',properties)
    # for data in jobData:
    #     data.pop('_id', None)
    #     # print(data)
    #     store_record(es,'site_jobs',data)
    # print(search('site_jobs','php'))