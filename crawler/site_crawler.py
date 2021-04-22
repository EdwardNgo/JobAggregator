# Bring your packages onto the path
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
sys.path.append(os.path.abspath(os.path.join('..', 'db_helper')))
sys.path.append('../')
print(sys.path)
from bs4 import BeautifulSoup
from utils import *
from db_helper import *
from data_extract import *
from datetime import datetime
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

    def get_site_attribute(self):
        return {
            'name':self.name,
            'urls':self.urls,
            "job_list_selector":self.job_list_selector,
            "img_selector":self.img_selector,
            "img_selector":self.title_selector,
            "company_selector":self.company_selector,
            "tags_selector":self.tags_selector,
            "time_selector":self.time_selector ,
            "location_selector":self.location_selector, 
            "main_section_selector":self.main_section_selector,
            "salary_selector":self.salary_selector 
        }

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
    # def get_pagniation_urls(url):
    #     page_num = 1
    #     while(True):
    #         res = retryRequest(url.format(page_num = page_num))
    #         if response.status_code != 200:
    #             break
    def get_generic_job(self):
        """
        Return in short for a job positions (title, location,company)
        """
        createDir('../data/{}'.format(self.name))
        insertdb = Job()
        for url in self.urls:
            page_num = 1
            # print(url)
            flag = True
            while(flag):
                response = retryRequest(url.format(page_num = page_num))
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                main_section = soup.select(self.main_section_selector)
                # print(len(main_section))
                jobs = []
                for item in main_section:
                    job = {'url':'','title':'','img':'','city':'','salary':'','update_time':'','company':'','month_year':''}
                    # compared_job =  {'url':'','title':'','img':'','city':'','salary':'','update_time':''}

                    job['url'] = getUrl(item,self.job_list_selector,url)
                    job['title'] = getTitle(item,self.title_selector)
                    job['img'] = getImg(item,self.img_selector)
                    job['city'] = getCity(item,self.location_selector)
                    job['salary'] = getSalary(item,self.salary_selector)
                    job['update_time'] = getUpdateTime(item,self.time_selector)
                    job['company'] = getCompany(item,self.company_selector,self.img_selector)
                    try:
                        job['month_year'] = getMonthYear(job['update_time'])
                    except:
                        pass
                    news_time = datetime.strptime(job['update_time'].replace("/20","/"),"%d/%m/%y")
                    current_day  = datetime.today()
                    delta = current_day - news_time
                    if(delta.days > 2):#neu tin duoc lay ma da ra truoc 2 ngay thi khong can phai lay nua -> tat ca cac tin sau cung the
                        flag = False
                        break
                    jobs.append(job)
                    # print(job)
                # print(jobs)

                insertdb.insertJobData(jobs,'test_raw_site_job')
                # save_jobs('../data/{}/{}.json'.format(self.name,url.format(page_num = page_num).split('/')[-1]),jobs)

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
