# Bring your packages onto the path
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'utils')))
sys.path.append('../')
print(sys.path)
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import requests
from utils import save_links,timeTransform,save_jobs

def retryRequest(urls):
    session = requests.Session()
    retry = Retry(connect=4, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(urls)

    return response

class Crawler(object):

    def __init__(self,name,urls,job_list_selector,img_selector,title_selector,company_selector,tags_selector,location_selector,time_selector,main_section_selector):
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
        for url in self.urls:
            page_num = 1
            while(True):
                response = retryRequest(url.format(page_num = page_num))
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                main_section = soup.select(self.main_section_selector)
                print(len(main_section))
                jobs = []
                for item in main_section:
                    job = {'url':'','title':'','img':'','city':'','salary':'','update_time':''}
                    compared_job =  {'url':'','title':'','img':'','city':'','salary':'','update_time':''}
                    if 'itviec' in url:
                        job['url'] = url.split('/it-jobs')[0] + item.select_one(self.job_list_selector)['href']
                    else:
                       job['url'] = item.select_one(self.job_list_selector)['href']

                    job['title'] = item.select_one(self.title_selector).text
                    job['img'] = item.select_one(self.img_selector)['data-src']
                    job['city'] = item.select_one(self.location_selector).text
                    job['update_time'] = timeTransform(item.select_one(self.time_selector).text)
                    if compared_job != job:
                        jobs.append(job)
                print(jobs)
                save_jobs('../data/{}/{}-{}.json'.format(self.name,url.split('/')[-2],page_num),jobs)

                if main_section == []:
                    break
                page_num += 1
    

if __name__ == '__main__':
    test = Crawler('itviec',['https://itviec.com/it-jobs/?page={page_num}'],'h2.title > a','div.logo-wrapper > a > img','h2.title','div.tag-list','','div.city > div >span','div.distance-time-job-posted > span','div.first-group > div')
    test.get_generic_job()
    # test2 = Crawler('topcv',['https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-c10131'],'h4.job-title > a','','','','','','')
    # techviec = 'ul.job_listings.job-list.full > li > a'
    # test2.get_all_job_list()