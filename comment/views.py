#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-13
#@Software : PyCharm
from flask import Blueprint,session,redirect,request
from models import Comments,Users,db

from config import COOKIE_NAME

from uuid import uuid1

comment = Blueprint('comment',__name__,template_folder = 'templates')

def checkUser():
    id = ''
    user = ''
    if 'id' in session:
        id = session['id']
    if id == '':
        id = request.cookies.get(COOKIE_NAME)
    users = Users.query.filter_by(id=id).all()
    if len(users) == 0:
        user = ''
    else:
        user = users[0]
    return user

@comment.route('/comment/create',methods = ['POST'])
def comment_create():
    user = checkUser()
    if user == '':
        return redirect('/')
    content = request.form.get('comment')
    print(content)
    answer_id = request.form.get('answer_id')
    print(answer_id)
    topic_id = request.form.get('topic_id')
    print(topic_id)
    c = Comments(id = str(uuid1()),user_id = user.id,answer_id = answer_id,content = content)
    db.session.add(c)
    db.session.commit()
    return redirect('/topic/' + topic_id)