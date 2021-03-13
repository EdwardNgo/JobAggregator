import json
import requests
import re
from collections import defaultdict
from dotenv import load_dotenv,find_dotenv
import os
load_dotenv(find_dotenv())
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
sys.path.append(os.path.abspath(os.path.join('..', 'db_helper')))
sys.path.append('../')
from db_helper import *
from utils import *

class ApiCrawler:
    def __init__(self,access_token,api_ver):
        self.access_token = access_token
        self.api_ver = api_ver
    def getGroupPosts(self,group_id,limit):
        insertdb = Job()
        fields = '?fields=feed.limit({limit})&access_token={access_token}'.format(limit = limit,access_token = self.access_token)
        url = self.api_ver + group_id + fields
        print(url)
        res = retryRequest(url)
        data = res.json()
        print(data)
        insertdb.insertJobData(data['feed']['data'],'fb_job')

if __name__ == "__main__":


    access_token = os.environ.get('access_token')
    print(access_token)
    groups = ['https://www.facebook.com/groups/30580654243953',
            'https://www.facebook.com/groups/174764463261090',
            'https://www.facebook.com/groups/2028704957422810','130580654243953']
    test =ApiCrawler(access_token,'https://graph.facebook.com/v10.0/')
    test.getGroupPosts('130580654243953',1000)

