import re
from datetime import datetime,timedelta
def timeTransform(str):
    value = int(re.search('\d+',str).group())
    print(value)
    if 's' in str or 'giay' in str:
        print('hi')
        return (datetime.now() - timedelta(seconds=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'h' in str or 'gio' in str:
        print('ha')
        return (datetime.now() - timedelta(hours=value)).strftime("%m/%d/%Y %H:%M:%S")
    if 'd' in str or 'ngay' in str:
        print('ho')
        return (datetime.now() - timedelta(days=value)).strftime("%m/%d/%Y %H:%M:%S")
    return str
if __name__ == '__main__':
    print(timeTransform('23h'))
    print(timeTransform('55d'))