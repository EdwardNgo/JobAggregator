from site_crawler import * 
def main():
    test = Crawler('itviec',
    ['https://itviec.com/it-jobs?page={page_num}'],
    'h2.title > a',
    'div.logo-wrapper > a > img',
    'h2.title',
    '',
    'div.tag-list',
    'div.city > div >span',
    'div.distance-time-job-posted > span',
    'div.first-group > div',
    '')
    test.get_generic_job()
if __name__ == "__main__":
    main()