#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-9
#@Software : PyCharm
from flask import Blueprint,redirect,session,request,render_template
from models import Topic,Users
from models import db
from config import COOKIE_NAME
from uuid import uuid1

import hashlib

topic = Blueprint('topic',__name__,template_folder = 'templates')

def md5(args):
    pwd = hashlib.md5(bytes('admin',encoding='utf-8'))
    pwd.update(bytes(args,encoding='utf-8'))
    return pwd.hexdigest()

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

@topic.route('/topic/created',methods = ['GET','POST'])
def topic_creata():
    user = checkUser()
    if user == '':
        return redirect('/')
    if request.method == 'GET':
        return render_template(
            'topicCreate.html',
            user = user
        )
    if request.method == 'POST':
        title = request.form.get('title')
        print(type(title))
        summary = request.form.get('summary')
        print(type(summary))
        content = request.args.get('content')
        print(len(content))
        print(type(content))
        topic = Topic(id = str(uuid1()),user_id = user.id,name = title,summary = summary,content = content)
        try:
            db.session.add(topic)
        except Exception as e:
            print(e)
        finally:
            db.session.commit()
        return redirect('/')