from site_crawler import * 
def main():
    print("Start Crawler 1")
    test = Crawler('itviec',
    ['https://itviec.com/it-jobs?page={page_num}'],
    'h2.title > a',
    'div.logo-wrapper > a > picture > img',
    'h2.title',
    '',
    'div.tag-list',
    'div.city > div >span',
    'div.distance-time-job-posted > span',
    'div.first-group > div',
    '',
    'div.job-details__paragraph')
    test.get_generic_job()
if __name__ == "__main__":
    main()