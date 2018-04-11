#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-9
#@Software : PyCharm
from flask import Blueprint,redirect,session,request,render_template
from models import Topic,Users,Anwser,Likes
from sqlalchemy import and_
from models import db
from config import COOKIE_NAME
from uuid import uuid1

import hashlib
import base64

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
def topic_create():
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
        summary = request.form.get('summary')
        content = request.form.get('content')
        topic = Topic(id = str(uuid1()),user_id = user.id,name = title,summary = summary,content = content)
        try:
            db.session.add(topic)
        except Exception as e:
            print(e)
        finally:
            db.session.commit()
        return redirect('/')

@topic.route('/topic/<id>',methods = ['GET','POST'])
def topic_detail(id):
    user = checkUser()
    topics = Topic.query.filter_by(id=id).all()
    if len(topics) == 0:
        topic = ''
    else:
        topic = topics[0]
    if request.method == 'GET':
        anwsersResult = Anwser.query.filter_by(topic_id=topic.id).order_by(Anwser.created_at.desc()).all()
        print(anwsersResult)
        answers = []
        for a in anwsersResult:
            like = Likes.query.filter(and_(Likes.user_id.like(user.id), Likes.comment_id.like(a.id))).all()
            if len(like):
                a.canLike = True
            else:
                a.canLike = False
            answers.append(a)
        print(answers)
        writer = Users.query.filter_by(id = topic.user_id).all()[0]
        return render_template(
            'topic.html',
            topic = topic,
            user = user,
            base64 = base64,
            writer = writer,
            anwsers = answers
        )
    if request.method == 'POST':
        content = request.form.get('content')
        print(content)
        ans = Anwser(id = str(uuid1()),user_id = user.id,topic_id = id,name = user.name,user_image = user.image,content = content)
        db.session.add(ans)
        db.session.commit()
        return redirect('/topic/' + topic.id)