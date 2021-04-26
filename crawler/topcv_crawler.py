from site_crawler import *

def main():
    print("Start Crawler 2")

    test2 = Crawler('topcv',
    ['https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-c10131?page={page_num}','https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026?page={page_num}','https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026?page={page_num}'],
    'h4.job-title > a',
    'div.row.job > div > a > img',
    'h4.job-title > a > span',
    'div.row-company > a',
    '',
    'div.row > div.col-sm-4.col-xs-6 > span',
    'div.updated_at.col-sm-4.col-xs-6',
    'div.job-list.search-result > div',
    '',
    'div.job-data')
    test2.get_generic_job()
    
if __name__ == '__main__':
    main()