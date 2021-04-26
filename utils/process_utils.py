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
    str = str.replace("\r","")
    str = str.replace("\n","")
    str = str.strip()
    str = re.sub("\s+"," ",str)
    return str.strip(' \n\r')

def cityNormalize(city):
    city = city.replace('Khu vực: ','')
    if 'Hà Nội' in city and 'Hồ Chí Minh' not in city or 'Ha Noi' in city:
        return 'Hà Nội'
    if 'Hồ Chí Minh' in city and 'Hà Nội' not in city or 'Ho Chi Minh' in city:
        return 'Tp Hồ Chí Minh'
    if 'Da Nang' in city:
        return 'Đà Nẵng'
    if city == '':
        return 'remote'
    return city

def getMonthYear(date_str):
    month = date_str.split('/')[1]
    if month[0] == '0':
        month = month.replace('0','')
    year = date_str.split('/')[2]
    return  month + '-' + year

def titleNormalize(title):
    it_title = ['python','frontend','Java','.Net','tester','data engineer','iOS','React Native','PHP','Nodejs','golang','Ui/Ux','Backend']
    for keyword in it_title:
        if keyword in title.lower():
            return keyword
    return title

def removeHtmlTag(text):
    TAG_RE = re.compile(r'<[^>]+>')
    text = text.replace("\n",'')
    text = TAG_RE.sub('.', text)
    text = re.sub("\.+",'.',text)
    return text.replace(':.','.')

if __name__ == '__main__':
    print(timeTransform('Cập nhật 2 tuần trước'))
    print(timeTransform('14h'))
    print(secondToDate('1614388687'))
    print(textNormalize('\r\n                    Senior Product Manager\r\n                                                                            '))
    print(textNormalize("Chuyên viên Phát triển Ứng dụng\r\n                                         (Mới)"))
    print(titleNormalize('nhân viên Tester'))
    print(removeHtmlTag("""<div class="job-details__paragraph">
<p><p>As a key member of the team, you’ll have a say in which employee perks we should provide you.</p><p><strong>REMUNERATION:</strong></p><ul><li>Competitive salary and excellent benefits</li><li>Bonus: performance and loyalty bonuses, team bonus, annual bonus (13th-month salary)</li><li>Salary review based on performance (every 3-6 months)</li></ul><p><strong>PERKS AND BENEFITS:</strong></p><ul><li>A cool and modern co-working space</li><li>Laptop + 2nd monitor</li><li><strong>Flexible working hours</strong></li><li><strong>5</strong> workdays/week, <strong>15</strong> paid vacation days/year</li><li>Parking allowance, unlimited snacks, and drinks</li><li>Bao Viet Healthcare insurance</li><li>Social insurance, medical insurance, unemployment insurance according to Vietnam Labor Law</li></ul><p><strong>DEVELOPMENT OPPORTUNITIES:</strong></p><ul><li>There’s <strong>unlimited potential for career growth</strong></li><li>Work in a vibrant and energetic space with startups and talented pros</li><li>Work for an international company with the <strong>potential for travel to Australia</strong></li></ul><p><strong>RECREATIONAL ACTIVITIES:</strong></p><ul><li>Annual company trip</li><li>Regular team building activities</li><li>Happy Fridays with discretional food and games</li></ul></p>
</div>"""))
    