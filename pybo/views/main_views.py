from flask import Blueprint, url_for
from werkzeug.utils import redirect

from flask_paginate import Pagination, get_page_parameter
from flask import request,render_template
import os, sqlite3
from  .. util.mySqlFunction import *

bp = Blueprint( 'main',__name__, url_prefix='/' )

@bp.route('/')
def index():
    return redirect( url_for('question._list'))


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo !'

@bp.route('/paging')
def paging():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10    
    page_info = {'page':page ,'per_page': per_page }
    q = request.args.get('q')
    search = True if q else False

    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pybo.db")
    subquerys = [ "select count(*) from question_voter where question.id = question_id",
                  "select count(*) from answer where question.id = question_id" ]

    sql = "select question.id,subject,user.username,question.create_date,(#subquery#) as voter,(#subquery#) as answer from question join user on question.user_id=user.id order by create_date desc"
    dataCnt, datas = get_datas_for_page_from_db( db_path, sql, page_info = page_info, subquerys = subquerys )
    pagination = Pagination(page=page,per_page=per_page, total=dataCnt, search=search, record_name='질문')

    return render_template('paging.html', question_list=datas, pagination=pagination )
