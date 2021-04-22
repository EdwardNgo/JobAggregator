import sys, os
os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'db_helper')))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'crawler')))
sys.path.append('../')
print(sys.path)
from crawler import careerbuilder_crawler,itviec_crawler,topcv_crawler,careerlink_crawler
from db_helper import siteDup
import _thread
import threading
from multiprocessing import Process
import sys
if __name__ == '__main__':
    # try:
    #     _thread.start_new_thread(careerbuilder_crawler.main() )
    #     _thread.start_new_thread(itviec_crawler.main())
    #     _thread.start_new_thread(topcv_crawler.main())
    #     _thread.start_new_thread(careerlink_crawler.main())
    # except:
    #     print ("Error: unable to start thread")
    p1 = Process(target = careerbuilder_crawler.main())
    p1.start()
    p2 = Process(target = itviec_crawler.main())
    p2.start()
    p3 = Process(target = topcv_crawler.main())
    p3.start()
    p4 = Process(target = careerlink_crawler.main())
    p4.start()
    #phai co join neu khong thi no van la sequential
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    siteDup('raw_site_job')