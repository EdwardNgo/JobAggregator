import re
from datetime import datetime,timedelta
import random

def timeTransform(str):
    try:
        value = int(re.search('\d+',str).group())
    except:
        return str

    if 's' in str or 'giây' in str:
        return (datetime.now() - timedelta(seconds=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'm' in str and str.split(' ') == 1 or 'phút' in str:
        return (datetime.now() - timedelta(minutes=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'h' in str and str.split(' ') == 1 or 'giờ' in str :
        return (datetime.now() - timedelta(hours=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'd' in str and str.split(' ') == 1 or 'ngày' in str :
        return (datetime.now() - timedelta(days=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'w' in str and str.split(' ') == 1 or 'tuần' in str:
        return (datetime.now() - timedelta(weeks=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'tháng' in str:
        return (datetime.now() - timedelta(weeks= 4*value + random.choice([2,3]))).strftime("%m/%d/%Y %H:%M:%S")

    return str

def secondToDate(value):
    return datetime.fromtimestamp(int(value)).strftime("%m/%d/%Y %H:%M:%S")

if __name__ == '__main__':
    print(timeTransform('Cập nhật 2 tuần trước'))
    print(timeTransform('55d'))
    print(secondToDate('1614388687'))