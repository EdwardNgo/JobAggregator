from site_crawler import *
def main():
    test4 = Crawler('careerbuilder',
    ['https://careerbuilder.vn/viec-lam/cntt-phan-mem-c1-trang-{page_num}-vi.html','https://careerbuilder.vn/viec-lam/cntt-phan-cung-mang-c63-trang-{page_num}-vi.html'],
    'a.job_link',
    'div.image > a > img',
    'a.job_link',
    'a.company-name',
    '',
    'div.location > ul > li',
    'div.time > time',
    'div.jobs-side-list > div > div',
    'div.salary > p')
    test4.get_generic_job()
if __name__ == '__main__':
    main()