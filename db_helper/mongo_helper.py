import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["JobAggregator"]

class Job(object):
    def __init__(self,client = pymongo.MongoClient("mongodb://localhost:27017/") ,db = pymongo.MongoClient("mongodb://localhost:27017/")["Job_Aggregator"]):
        self.client = client
        self.db = db

    def insertJobData(self,data,colname):
        col = self.db[f'{colname}']
        try:
            col.insert_many(data)
            print("Insert Successfully")
        except Exception as e:
            print(e)
    def getJobData(self,colname):
        col = self.db[f'{colname}']
        cursor = col.find()
        data = []
        for document in cursor:
            data.append(document)
        return data
    def removeDuplicateData(self,colname):
        col = self.db[f'{colname}']
        # col.aggregate([ { "$group":{ _id:{company:"$company",city:"$city",title:"$title"}, DuplicateValueIds:{$addToSet:"$_id"} } } ])
        pass
            
if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["JobAggregator"]
    print(mydb)
    jobinsert = Job()
    # jobinsert.insertJobData([{'a':1},{'b':2}],'fb_job')
    jobinsert.removeDuplicateData('site_job')