#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-9
#@Software : PyCharm
from flask import Blueprint,redirect,session,request,render_template
from models import Topic,Users,Answer,Likes,Comments
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
            user = user,
            base64 = base64
        )
    if request.method == 'POST':
        title = request.form.get('title')
        summary = request.form.get('summary')
        content = request.form.get('content')
        topic = Topic(id = str(uuid1()),user_id = user.id,name = title,summary = summary,content = content)
        topic_count = user.topic_count + 1
        Users.query.filter_by(id = user.id).update({'topic_count':topic_count})
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
        page = request.args.get('page_ans', 1, type=int)
        pagination_ans = Answer.query.filter_by(topic_id=topic.id).paginate(page, per_page=1, error_out=False)
        writer = Users.query.filter_by(id=topic.user_id).all()[0]
        if len(pagination_ans.items) == 0:
            return render_template(
                'topic.html',
                topic=topic,
                user=user,
                base64=base64,
                writer=writer,
            )
        else:
            answer = pagination_ans.items[0]
            comments = Comments.query.filter_by(answer_id=answer.id).all()
            comment = []
            for c in comments:
                user = Users.query.filter_by(id=c.user_id).all()[0]
                c.user_name = user.name
                comment.append(c)
            like = Likes.query.filter(and_(Likes.user_id.like(user.id), Likes.comment_id.like(answer.id))).all()
            if len(like):
                answer.canLike = True
            else:
                answer.canLike = False
            u = Users.query.filter_by(id = answer.user_id).all()[0]
            answer.user_name = u.name
            answer.user_image = u.image
            return render_template(
                'topic.html',
                topic = topic,
                user = user,
                base64 = base64,
                writer = writer,
                anwsers = answer,
                pagination_ans=pagination_ans,
                comment = comment
            )
    if request.method == 'POST':
        content = request.form.get('content')
        answer_count = user.answer_count + 1
        Users.query.filter_by(id = user.id).update({'answer_count':answer_count})
        ans = Answer(id = str(uuid1()),user_id = user.id,topic_id = id,content = content)
        db.session.add(ans)
        db.session.commit()
        return redirect('/topic/' + topic.id)

@topic.route('/topic/delete/<id>')
def topic_delete(id):
    user = checkUser()
    if user == '':
        return redirect('/')
    t = Topic.query.filter_by(id = id).all()[0]
    answer = Answer.query.filter_by(topic_id = id).all()
    print(answer)
    if len(answer):
        for a in answer:
            db.session.delete(a)
    db.session.delete(t)
    db.session.commit()
    return redirect('/person/'+user.id)