import logging
from elasticsearch import Elasticsearch,helpers
from mongo_helper import *
import requests
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },

        
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

def mongoToEs(colname,index_name):
    job = Job()
    jobData = job.getJobData(colname)
    es = connect_elasticsearch() 

    create_index(es,index_name)
    for data in jobData:
        # print(data)
        # print(data)
        data['id'] = str(data['_id'])
        data.pop("_id", None)
        store_record(es,index_name,data)


def genMongoData(colname):
    myclient = MongoClient("mongodb://188.166.228.248:27017/")
    mydb = myclient["newsbuzzer"]
    col = mydb[colname]
    cursor = col.find({}).limit(1000)
    data = []
    for doc in cursor:
        yield doc

def mongoToEs2(colname,index_name,limit = 1000):
    myclient = MongoClient("mongodb://188.166.228.248:27017/")
    mydb = myclient["newsbuzzer"]
    col = mydb[colname]
    cursor = col.find({}).limit(limit)
    es = connect_elasticsearch() 
    create_index(es,index_name)
    for data in cursor:
        data['id'] = str(data['_id'])
        data.pop("_id", None)
        store_record(es,index_name,data)

def search(index_name,field):
    es = connect_elasticsearch()
    # client = Search(using  = es.index(index = index_name))
    # q = Match(field={"query": "đốt"})
    # s = client.query(q)
    # resp = s.execute()
    # resp = es.search(index=index_name, body = {"query": {"match": {field:"đốt"}}})
    resp = es.search(index=index_name, body = {"query": {"multi_match":{"query":"đốt","fields":["body_tokenized",field]}}})

    return resp
if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    # mongoToEs('new_raw_site_job','new_raw_site_job')
    # mongoToEs('fb_job','fb_job')
    mongoToEs2('raw_article',"raw_article_2",10000)
    # print(search('site_jobs','php'))
    # print(search('raw_article_2','title_tokenized'))