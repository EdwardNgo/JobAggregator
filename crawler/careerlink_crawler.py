from site_crawler import *
def main():
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

if __name__ == '__main__':
    main()