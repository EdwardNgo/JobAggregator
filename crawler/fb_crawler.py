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
from datetime import datetime
import redis
import time
import logging
redisClient = redis.Redis("123.31.43.115",6379,password   ='GX1cnNgdXfCNUbYKa3' ,db=1)

class ApiCrawler:
    def __init__(self,access_token,api_ver):
        self.access_token = access_token
        self.api_ver = api_ver

    def getGroupPosts(self,group_id,limit):
        insertdb = Job()
        news = Job()
        fields = '?fields=feed.limit({limit})&access_token={access_token}'.format(limit = limit,access_token = self.access_token)
        # fields = "/feed?fields=message,updated_time,full_picture&limit={limit}&access_token={access_token}".format(limit = limit,access_token = self.access_token)
        url = self.api_ver + group_id + fields
        print(url)
        res = retryRequest(url)
        data = res.json()
        print(data)
        # fbjobdata = data['feed']['data']
        # fbjobdata['published'] = fbjobdata['updated_time']
        # print(fbjobdata)
        insertdb.insertJobData(data['feed']['data'],'fb_job')


    def saveNewsToCache(self,group_id,limit):
        fields = "/feed?fields=message,updated_time,full_picture&limit={limit}&access_token={access_token}".format(limit = limit,access_token = self.access_token)
        url = self.api_ver + group_id + fields
        print(url)
        res = retryRequest(url)
        if res.status_code != 200:
            return
        data = res.json()
        newpost = 0
        try:
            for post in data['data']:
                #xu ly thoi gian ra timestamp
                ele = post['updated_time'].replace("T"," ").replace("+0000","")
                ele = datetime.strptime(ele,"%Y-%m-%d %H:%M:%S")
                timestamp = datetime.timestamp(ele)

                post_id = post['id'].split("_")[1]

                #check xem bai viet da duoc crawl chua  
                if redisClient.hget(group_id,post_id) != None:
                    print(post_id + " has been crawled")
                    continue # crawl roi thi crawl bai khac
                else:
                    # print(post_id)
                    newpost += 1
                    transformed = {"content":"","img":"","timestamp":""}
                    transformed['content'] = post['message']
                    try:
                        transformed['img'] = post['full_picture']
                    except:
                        print("Picture not found")
                        transformed['img'] = ''
                    print(post_id)
                    transformed['timestamp'] =  timestamp  
                    transformed = json.dumps(transformed)
                    # print(transformed)
                    redisClient.hset(group_id,post_id,transformed)
        except Exception as e:
            print(e)
        print("Crawled: " + str(newpost) +  " new posts!")
            # redisClient.hset(group_id,transformed)
        # print(groupposts)

def getAccessToken():
    print('\n** < GET FB ACCESS TOKEN FROM COOKIE > **\n')
    cookie = "sb=9hkQYARdzQVl3vjvJ9U1ZjsA; m_pixel_ratio=1; _fbp=fb.1.1614905941345.1557415172; x-referer=eyJyIjoiL2dyb3Vwcy9weXRob25jb21tdW5pdHl2bi9wZXJtYWxpbmsvMzU5NDE2MjE5NDA1NzgwNC8%2FZnM9MSZmb2N1c19jb21wb3Nlcj0wIiwiaCI6Ii9ncm91cHMvcHl0aG9uY29tbXVuaXR5dm4vcGVybWFsaW5rLzM1OTQxNjIxOTQwNTc4MDQvP2ZzPTEmZm9jdXNfY29tcG9zZXI9MCIsInMiOiJtIn0%3D; c_user=100033803722425; datr=Qq5xYMEwvygqBshrX7MFgKHw; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1619267492029%2C%22v%22%3A1%7D; spin=r.1003681751_b.trunk_t.1619347232_s.1_v.2_; xs=25%3AxQQ_eXlRedz1Mw%3A2%3A1618062912%3A14236%3A6303%3A%3AAcVmKlxQ_ikbaijxSD2e_KQkGG7aTCT066_-Xu1I37Q; fr=1afI3TAIORWOQ0blx.AWUzwKxkyMgS35KbI3_l8iMdxnM.BghYld.DO.AAA.0.0.BghYld.AWXtQh1YJsg"
    try:
        data = requests.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed#_=_', headers = {
            'user-agent'                : 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', # don't change this user agent.
            'referer'                   : 'https://m.facebook.com/',
            'host'                      : 'm.facebook.com',
            'origin'                    : 'https://m.facebook.com',
            'upgrade-insecure-requests' : '1',
            'accept-language'           : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control'             : 'max-age=0',
            'accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type'              : 'text/html; charset=utf-8'
        }, cookies = {
            'cookie'                    : cookie
        })
        find_token = re.search('(EAAA\w+)', data.text)
        # results    = '\n* Fail : maybe your cookie invalid !!' if (find_token is None) else '\n* Your fb access token : ' + find_token.group(1)
        if (find_token is None):
            results = None
        else:
            results = find_token.group(1)
    except requests.exceptions.ConnectionError:
        results    = '\n* Fail : no connection here !!'
    except:
        results    = '\n* Fail : unknown errors, please try again !!'

    return results


if __name__ == "__main__":

    while True:
        print("hi")
        access_token = getAccessToken()
        print(access_token)
        if (access_token.startswith('EAA')):
            # print(access_token)
            groups = ['174764463261090','2028704957422810','130580654243953']
            # groups = ['929563144068596']
            test =ApiCrawler(access_token,'https://graph.facebook.com/v10.0/')
            for group in groups:
                # try:
                test.getGroupPosts(group,100)
                # except Exception as e:
                #     print(e)
        else:
            print("token not found")
        time.sleep(600)
    # resp =redisClient.hget('929563144068596','1495701634121408')
    # resp = redisClient.hgetall('929563144068596')
    # # print(resp)
    # print(len(redisClient.hkeys("929563144068596")))