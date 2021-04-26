from flask import Flask, Blueprint, flash, g, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
import sys,os
sys.path.append(os.path.abspath(os.path.join("..", 'utils')))
sys.path.append(os.path.abspath(os.path.join("..", 'db_helper')))
sys.path.append('../')
from db_helper import *
from bson.json_util import dumps
from bson.objectid import ObjectId
import re

app = Flask(__name__)
job = Job()

def get_job(data,offset = 0,per_page = 25):
    return data[offset:offset+per_page]


@app.route('/')
def index():
    jobData = job.getJobData('new_raw_site_job')
    print(jobData)
    # newData = []
    # for data in jobData:
    #     data['converted_id'] = str(data['_id']).replace('1','A').replace('2','b').replace('3','c').replace('4','d').replace('5','e').replace('6','f').replace('7','g').replace('8','h').replace('9','i').replace('0','k')
    #     newData.append(data)
    # print(data)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(jobData)
    pagination_jobData = get_job(jobData,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',
                           jobData=pagination_jobData,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/search',methods = ['POST'])
def search():
    if request.method == "POST":
        query = request.form['query']
        print(query)
        query_res = search_record('new_raw_site_job',query)
        return render_template('search.html',queryData = query_res)
    return render_template('index.html')

@app.route('/search_fb',methods = ['POST'])
def search_fb():
    if request.method == "POST":
        query = request.form['query_fb']
        print(query)
        query_res = search_record('fb_job',query)
        print(query_res)
        format_query_res = []
        for data in query_res:
            print(data)
            try:
                data['splitted_message'] = data['message'].split('\n')
            except:
                data['splitted_message'] = []
            format_query_res.append(data)
        return render_template('search_fb.html',queryData = format_query_res)
    return render_template('index.html')

@app.route('/fb_rec',methods = ['GET','POST'])
def fb():
    fbJobData = job.getJobData('fb_job')
    print(fbJobData)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(fbJobData)
    pagination_jobData = []
    for data in fbJobData:
        print(data)
        try:
            data['splitted_message'] = data['message'].split('\n')
        except:
            data['splitted_message'] = []
        pagination_jobData.append(data)
    pagination_jobData = get_job(fbJobData,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    print(pagination_jobData)
    return render_template('facebook.html',
                           jobData=pagination_jobData,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
# @app.route('/analytics',methods=['GET', 'POST'])
# def analytics():
#     topCompany = simpleAnalyse('raw_site_job','company')
#     topRegion = simpleAnalyse('raw_site_job','location')
#     topTitle = simpleAnalyse('raw_site_job','title')
#     print(topCompany)
#     return render_template('analytics.html',topCompany=topCompany)

@app.route('/analytics',methods = ['GET', 'POST'])
def analytics():

    
    # getKPIUsers = {
    #         'totalUsers': 200,
    #         'recent24hUsers': 24,
    #         'recentWeekusers': 48
    # }

    #phan tich cong ty tuyen nhieu nhat den hien tai
    topCompany = simpleAnalyse('new_raw_site_job','company',top = 10)
    companyLabel = list(topCompany.keys())
    recruitValue = list(topCompany.values())
    #phan tich viec lam theo thanh pho
    topCity = simpleAnalyse('new_raw_site_job','city',top  = 5)
    cityLabel  = list(topCity.keys())
    cityValue = list(topCity.values())
    #thong ke luong tin tuyen dung theo ngay
    dailyRecruitment = recruitmentByDay('new_raw_site_job','4-2021')
    dailyRecruitmentLabel = list(dailyRecruitment.keys())
    dailyRecruitmentValue = list(dailyRecruitment.values())
    print(dailyRecruitment)
    # print(topCompany)
    # print(list(companyLabel))
    #thong ke ten cac vi tri hay duoc tuyen dung
    topTitle = simpleAnalyse('new_raw_site_job','title',top= 20)
    topTitleLabel = list(topTitle.keys())
    print(topTitleLabel)
    topTitleValue = list(topTitle.values())
    print(topTitle)
    return render_template("analytics.html",
                    recruitValue=recruitValue,companyLabel=companyLabel,
                    cityValue = cityValue,cityLabel = cityLabel,
                    dailyRecruitmentLabel = dailyRecruitmentLabel,dailyRecruitmentValue = dailyRecruitmentValue,
                    topTitleLabel = topTitleLabel,topTitleValue = topTitleValue,)

@app.route("/site_job/<id>",methods = ["GET"])
def jobById(id):
    resp = job.getJobById('new_raw_site_job',id)
    json_resp = json.loads(resp)
    if 'details' not in json_resp.keys():
        json_resp['details'] =['Khong co thong tin cho job nay. Xem them tai: ' ,json_resp['url']]
    json_resp['cleaned_text'] = []
    for data in json_resp['details']:
        print(data)
        data.replace(". .","").replace(".}","").replace("}","").strip(".").strip(".}")
        json_resp['cleaned_text'].append(data)
    # print(json_resp)
    # print(re.split('\.+',json_resp['cleaned_text']))
    return render_template("details.html",job = json_resp)

if __name__ == '__main__':
    app.run(debug=True)