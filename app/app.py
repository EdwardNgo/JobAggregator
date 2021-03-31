from flask import Flask, Blueprint, flash, g, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
import sys,os
sys.path.append(os.path.abspath(os.path.join("..", 'utils')))
sys.path.append(os.path.abspath(os.path.join("..", 'db_helper')))
sys.path.append('../')
from db_helper import *

app = Flask(__name__)
job = Job()

def get_job(data,offset = 0,per_page = 25):
    return data[offset:offset+per_page]


@app.route('/')
def index():
    jobData = job.getJobData('site_job')
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
        query_res = search_record('site_jobs',query)
        return render_template('search.html',queryData = query_res)
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
@app.route('/analytics',methods=['GET', 'POST'])
def analytics():
    return render_template('analytics.html')
if __name__ == '__main__':
    app.run(debug=True)