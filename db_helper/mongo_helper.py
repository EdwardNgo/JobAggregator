import pymongo
from pymongo import MongoClient
from collections import OrderedDict
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["JobAggregator"]
from datetime import datetime
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import pandas as pd

client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')

class Job(object):
    def __init__(self,client = MongoClient("mongodb://localhost:27017/") ,db = MongoClient("mongodb://localhost:27017/")["Job_Aggregator"]):
        self.client = client
        self.db = db

    def insertJobData(self,data,colname):
        col = self.db[colname]
        try:
            col.insert_many(data)
            print("Insert Successfully")
        except Exception as e:
            # col.insert_one(data)
            print(e)

    def getJobData(self,colname):
        col = self.db[colname]
        # col.updateMany({},{"$set":{"id":ObjectId})
        cursor = col.aggregate([{
        '$sort': {
            'published': -1,
            'updated_time':-1
        }
        }
        ])
        data = []
        for document in cursor:
            data.append(document)
        return data

    def getJobById(self,colname,id):
        col = self.db[colname]
        cursor = col.find_one({'_id':ObjectId(id)})
        resp = dumps(cursor)
        return resp

#xoa ban ghi trung lap
def siteDup(collection_name):

    result = client['Job_Aggregator'][collection_name].aggregate([
        {
            '$group': {
                '_id': {
                    'city': '$city', 
                    'title': '$title', 
                    'company': '$company'
                }, #group theo cac thuoc tinh
                'dups': {
                    '$addToSet': '$_id'
                }, #truong dup chua cac objectId
                'count': {
                    '$sum': 1#dem so ban ghi trung nhau
                }
            }
        }, {
            '$match': {
                'count': {
                    '$gt': 1#lay ban ghi co sum > 1(khong unique)
                }
            }
        }
    ])
    for i in result:
        print(i)
        print(i['dups'][1:])
        client['Job_Aggregator'][collection_name].delete_many({"_id":{"$in": i['dups'][1:]}})#xoa tru mot ban ghi trong dup

def getRegionJobCount(collection_name):
    pipeline = [{"$group":
                        {"_id":
                            {"city":"$city","month_year":"$month_year"},
                            "job_count":{"$sum":1}
                        }
                }]
    result = client['Job_Aggregator'][collection_name].aggregate(pipeline)
    list_cur = list(result)
    json_data = dumps(list_cur)
    # # with open("test.json", "w") as f:
    # #     json.dump(json.loads(json_data), f,ensure_ascii = False,indent  = 4)
    json_data = json.loads(json_data)
    return json_data

def simpleAnalyse(collection_name,field,month='6-2021',top=5):
    client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    cursor = client['Job_Aggregator'][collection_name].aggregate([
        {
            '$match': {
                'month_year': {
                    '$eq': f'{month}'
                }
            }
        },
        {
            '$group': {
                '_id': {
                    f'{field}': f'${field}'
                }, # tinh so luong tin tuyen dung theo tung thang
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                'count': -1
            }
        }
    ])
    result = []
    incrField = dict()

    for i in cursor:
        result.append(i)
    for res in result[:top]:
        incrField[res['_id'][field]] = res['count']

    return incrField
def recruitmentByDay(collection_name,month):
    client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    cursor = client['Job_Aggregator'][collection_name].aggregate([
        {
            '$match': {
                'month_year': {
                    '$eq': f'{month}'
                }
            }
        }, {
            '$group': {
                '_id': {
                    'month_year': '$month_year', 
                    'month_year': '$update_time'
                }, 
                'count': {
                    '$sum': 1
                }
            }
        }
    ])
    incrDayList = []
    for i in cursor:
        incrDay = dict()
        incrDay['Date'] = i['_id']['month_year']
        incrDay['numberOfRecruit'] = i['count']
        incrDayList.append(incrDay)
    # print(incrDayList)
    incrDayList.sort(key = lambda x:x['Date'])#phai sort theo ngay tu dau thang den cuoi thang
    day_dict = dict()
    for day in incrDayList:
        day_dict[day['Date']] = day['numberOfRecruit']#format ve dang de ve bieu do
    return day_dict
if __name__ == '__main__':
    # myclient = MongoClient("mongodb://localhost:27017/")
    # mydb = myclient["JobAggregator"]
    # print(mydb)
    # jobinsert = Job()
    # # jobinsert.insertJobData([{'a':1},{'b':2}],'fb_job')
    # jobinsert.removeDuplicateData('site_job')
    # print(simpleAnalyse('raw_site_job','company'))
    # data = []
    # for i in ['1-2021','2-2021','3-2021','4-2021','5-2021']:
    #     _,res = recruitmentByDay('new_raw_site_job',i)
    #     print(res)
    #     data += res
    # df = pd.json_normalize(data)
    # df.to_csv("test.csv")
    print(getRegionJobCount("new_raw_site_job"))