# Bring your packages onto the path
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
sys.path.append('../')
print(sys.path)
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
from utils import save_links,timeTransform,save_jobs,secondToDate, createDir

def retryRequest(urls):
    session = requests.Session()
    retry = Retry(connect=4, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(urls)

    return response

class Crawler(object):

    def __init__(self,name,urls,job_list_selector,img_selector,title_selector,company_selector,tags_selector,location_selector,time_selector,main_section_selector,salary_selector):
        self.name = name
        self.urls = urls
        self.job_list_selector = job_list_selector
        self.img_selector = img_selector
        self.title_selector = title_selector
        self.company_selector = company_selector
        self.tags_selector = tags_selector
        self.time_selector = time_selector
        self.location_selector = location_selector
        self.main_section_selector = main_section_selector
        self.salary_selector = salary_selector

    def get_all_job_list(self):
        """
        Return the links of job position in website
        """
        job_urls = []
        for url in self.urls:
            page_num = 1
            while(True):
                response = retryRequest(url.format(page_num = page_num))
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                job_link_div = soup.select(self.job_list_selector)
                if 'itviec' in url:
                    links = [url.split('/it-jobs')[0] + div['href'] for div in job_link_div]
                else:
                    links = [div['href'] for div in job_link_div]
                if links == []:
                    break
                save_links('../data/{}/{}-{}.txt'.format(self.name,url.split('/')[-2],page_num),links)
                page_num += 1


        return job_urls
    
    def get_detail_job(self,job_urls):
        """
        Return the Job Description of a job
        """
        return
    
    def get_generic_job(self):
        """
        Return in short for a job positions (title, location,company)
        """
        createDir('../data/{}'.format(self.name))
        for url in self.urls:
            page_num = 1
            print(url)
            while(True):
                response = retryRequest(url.format(page_num = page_num))
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                main_section = soup.select(self.main_section_selector)
                print(len(main_section))
                jobs = []
                for item in main_section:
                    job = {'url':'','title':'','img':'','city':'','salary':'','update_time':'','company':''}
                    compared_job =  {'url':'','title':'','img':'','city':'','salary':'','update_time':''}
                    if 'itviec' in url:
                        job['url'] = url.split('/it-jobs')[0] + item.select_one(self.job_list_selector)['href']
                    if 'careerlink' in url:
                        job['url'] = url.split('/viec-lam')[0] + item.select_one(self.job_list_selector)['href']
                    else:
                       job['url'] = item.select_one(self.job_list_selector)['href']

                    job['title'] = item.select_one(self.title_selector).text
                    try:
                        job['img'] = item.select_one(self.img_selector)['data-src']
                    except:
                        job['img'] = item.select_one(self.img_selector)['src']

                    try:
                        job['city'] = item.select_one(self.location_selector).text
                    except:
                        job['city'] = ''

                    try:
                        job['update_time'] = secondToDate((item.select_one(self.time_selector))['data-datetime'])
                    except:
                        job['update_time'] = timeTransform(item.select_one(self.time_selector).text)
                        print(item.select_one(self.time_selector).text)

                    try:
                        job['company'] = item.select_one(self.company_selector).text
                    except:
                        job['company'] = item.select_one(self.img_selector)['alt']

                    try:
                        job['salary'] = item.select_one(self.salary_selector).text
                    except:
                        job['salary'] = ''

                    if compared_job != job:
                        jobs.append(job)
                    # print(job)
                print(jobs)
                save_jobs('../data/{}/{}.json'.format(self.name,url.format(page_num = page_num).split('/')[-1]),jobs)

                if main_section == []:
                    break
                page_num += 1
    

if __name__ == '__main__':
    # test = Crawler('itviec',
    # ['https://itviec.com/it-jobs?page={page_num}'],
    # 'h2.title > a',
    # 'div.logo-wrapper > a > img',
    # 'h2.title',
    # '',
    # 'div.tag-list',
    # 'div.city > div >span',
    # 'div.distance-time-job-posted > span',
    # 'div.first-group > div',
    # '')
    # test.get_generic_job()

    # test2 = Crawler('topcv',
    # ['https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-c10131?page={page_num}','https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026?page={page_num}','https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026?page={page_num}'],
    # 'h4.job-title > a',
    # 'div.row.job > div > a > img',
    # 'h4.job-title > a > span',
    # 'div.row-company > a',
    # '',
    # 'div.row > div.col-sm-4.col-xs-6 > span',
    # 'div.updated_at.col-sm-4.col-xs-6',
    # 'div.job-list.search-result > div',
    # '')
    # test2.get_generic_job()

    test3 = Crawler('careerlink',
    ['https://www.careerlink.vn/viec-lam/cntt-phan-cung-mang/130?page={page_num}','https://www.careerlink.vn/viec-lam/cntt-phan-mem/19?page={page_num}'],
    'a.job-link.clickable-outside',
    'div.media.p-3.p-lg-4 > div >img',
    'a.job-link.clickable-outside > h5',
    'a.text-dark.job-company.mb-1.d-inline-block.line-clamp-1',
    '',
    'div.list-with-comma > a.text-reset',
    'span.cl-datetime',
    'ul.list-group.mt-4 > li',
    'span.job-salary.text-primary')
    test3.get_generic_job()

    # test4 = Crawler('careerbuilder',
    # ['https://careerbuilder.vn/viec-lam/cntt-phan-mem-c1-trang-{page_num}-vi.html','https://careerbuilder.vn/viec-lam/cntt-phan-cung-mang-c63-trang-{page_num}-vi.html'],
    # 'a.job_link',
    # 'div.image > a > img',
    # 'a.job_link',
    # 'a.company-name',
    # '',
    # 'div.location > ul > li',
    # 'div.time > time',
    # 'div.jobs-side-list > div > div',
    # 'div.salary > p')
    # test4.get_generic_job()
