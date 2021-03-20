from flask import Flask, Blueprint, flash, g, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args
import sys,os
sys.path.append(os.path.abspath(os.path.join("..", 'utils')))
sys.path.append(os.path.abspath(os.path.join("..", 'db_helper')))
sys.path.append('../')
from db_helper import *

app = Flask(__name__)
job = Job()
jobData = job.getJobData('site_job')
print(len(jobData))

def get_job(offset = 0,per_page = 25):
    return jobData[offset:offset+per_page]

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')
@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(jobData)
    pagination_jobData = get_job(offset=offset, per_page=per_page)
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
if __name__ == '__main__':
    app.run(debug=True)