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
import datetime
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
        fbjobdata = data['feed']['data']
        fbjobdata['published'] = fbjobdata['updated_time']
        print(data)
        insertdb.insertJobData(data['feed']['data'],'fb_job')

# def getAccessToken():
#     url = "https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed"
#     headers = {"cookies" :"c_user=100033803722425;xs=40%3AU4MLreUCe4JHug%3A2%3A1617073939%3A14236%3A6303%3A%3AAcWc_6tMlyikNN_tNiOGWGN0HlKmgPVfU_L2ys4wCg;","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

#     res = requests.get(url,headers = headers)
#     return res.content
    
def getAccessToken():
    print('\n** < GET FB ACCESS TOKEN FROM COOKIE > **\n')
    cookie = "sb=9hkQYARdzQVl3vjvJ9U1ZjsA; m_pixel_ratio=1; _fbp=fb.1.1614905941345.1557415172; x-referer=eyJyIjoiL2dyb3Vwcy9weXRob25jb21tdW5pdHl2bi9wZXJtYWxpbmsvMzU5NDE2MjE5NDA1NzgwNC8%2FZnM9MSZmb2N1c19jb21wb3Nlcj0wIiwiaCI6Ii9ncm91cHMvcHl0aG9uY29tbXVuaXR5dm4vcGVybWFsaW5rLzM1OTQxNjIxOTQwNTc4MDQvP2ZzPTEmZm9jdXNfY29tcG9zZXI9MCIsInMiOiJtIn0%3D; c_user=100033803722425; datr=Qq5xYMEwvygqBshrX7MFgKHw; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1619267492029%2C%22v%22%3A1%7D; spin=r.1003681751_b.trunk_t.1619347232_s.1_v.2_; xs=25%3AxQQ_eXlRedz1Mw%3A2%3A1618062912%3A14236%3A6303%3A%3AAcVmKlxQ_ikbaijxSD2e_KQkGG7aTCT066_-Xu1I37Q; fr=1afI3TAIORWOQ0blx.AWUzwKxkyMgS35KbI3_l8iMdxnM.BghYld.DO.AAA.0.0.BghYld.AWXtQh1YJsg"
    cookie2 = "sb=dRcUYGUlNU7KnqEGLngBQ5_S; datr=dRcUYBfjkZFOJMaX3yH8tO-6; c_user=100012462527820; presence=C%7B%22t3%22%3A%5B%7B%22i%22%3A%22u.100005633893433%22%7D%2C%7B%22i%22%3A%22g.4122135711153071%22%7D%2C%7B%22i%22%3A%22p.2276249655987344%22%7D%2C%7B%22i%22%3A%22u.100009516524246%22%7D%2C%7B%22i%22%3A%22p.110117883887364%22%7D%2C%7B%22i%22%3A%22g.2965558100213255%22%7D%5D%2C%22utc3%22%3A1617162569505%2C%22v%22%3A1%7D; spin=r.1003553351_b.trunk_t.1617288463_s.1_v.2_; xs=42%3AccAm1QA-11Cs2g%3A2%3A1611929480%3A14236%3A6338%3A%3AAcXh05UfBC56glRnlJBovqwocarnBPuuQisHtAM3Zxc; fr=1c1Fit7ZfGnl54biy.AWVNACPdz-Tf6lWDTc3WWMlseJw.BgZd0S.Yd.AAA.0.0.BgZd0S.AWUtxbvxb2c"
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


    access_token = os.environ.get('access_token')
    access_token = getAccessToken()
    print(access_token)
    if (access_token.startswith('EAA')):
        print(access_token)
        groups = ['30580654243953',
                '174764463261090',
                '2028704957422810','130580654243953']
        test =ApiCrawler(access_token,'https://graph.facebook.com/v10.0/')
        for group in groups:
            try:
                test.getGroupPosts(group,1000)
            except Exception as e:
                print(e)
    else:
        print("token not found")
