import re
from datetime import datetime,timedelta
import random

def timeTransform(str):
    try:
        value = int(re.search('\d+',str).group())
    except:
        return str

    if 's' in str or 'giây' in str:
        return (datetime.now() - timedelta(seconds=value)).strftime("%d/%m/%Y")
    if 'm' in str and len(str.split(' ')) == 1 or 'phút' in str:
        return (datetime.now() - timedelta(minutes=value)).strftime("%d/%m/%Y")
    if 'h' in str and len(str.split(' ')) == 1 or 'giờ' in str :
        return (datetime.now() - timedelta(hours=value)).strftime("%d/%m/%Y")
    if 'd' in str and len(str.split(' ')) == 1 or 'ngày' in str :
        return (datetime.now() - timedelta(days=value)).strftime("%d/%m/%Y")
    if 'w' in str and len(str.split(' ')) == 1 or 'tuần' in str:
        return (datetime.now() - timedelta(weeks=value)).strftime("%d/%m/%Y")
    if 'tháng' in str:
        return (datetime.now() - timedelta(weeks= 4*value + random.choice([2,3]))).strftime("%d/%m/%Y")

    return str

def secondToDate(value):
    return datetime.fromtimestamp(int(value)).strftime("%d/%m/%Y")

def textNormalize(str):
    return str.strip(' \n\r')

if __name__ == '__main__':
    print(timeTransform('Cập nhật 2 tuần trước'))
    print(timeTransform('14h'))
    print(secondToDate('1614388687'))
    print(textNormalize('\r\n                    Senior Product Manager\r\n                                                                            '))