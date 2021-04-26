import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
from utils import *
from bs4 import BeautifulSoup

def getUrl(item,selector,url):
    if 'itviec' in url:
        return url.split('/it-jobs')[0] + item.select_one(selector)['href']
    elif 'careerlink' in url:
        return url.split('/viec-lam')[0] + item.select_one(selector)['href']
    else:
        # print('ha')
        return item.select_one(selector)['href']
    return ''

def getTitle(item,selector):
    return titleNormalize(textNormalize(item.select_one(selector).text))

def getImg(item,selector):
    try:
        return item.select_one(selector)['data-src']
    except:
        return item.select_one(selector)['src']

def getCity(item,selector):
    try:
        return cityNormalize(textNormalize(item.select_one(selector).text))
    except:
        return ''

def getUpdateTime(item,selector):
    try:
        #mot so trang se co dang x/y/z
        return secondToDate((item.select_one(selector))['data-datetime'])
    except:
        # print(timeTransform(item.select_one(selector).text))
        return timeTransform(item.select_one(selector).text)

        
def getCompany(item,selector1,selector2):
    try:
        return textNormalize(item.select_one(selector1).text)
    except:
        #thuong thi ten cong ty se co trong anh
        return textNormalize(item.select_one(selector2)['alt'])

def getSalary(item,selector):
    try:
        return textNormalize(item.select_one(selector).text)
    except:
        return ''

