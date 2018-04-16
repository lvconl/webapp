#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-14
#@Software : PyCharm
from flask import Blueprint,request,session,make_response,render_template,redirect
from models import Friends,Users,db,Topic,Answer

from uuid import uuid1
from config import COOKIE_NAME

import base64

person = Blueprint('person',__name__,template_folder = '../user/templates')


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

@person.route('/person/follow/<id>')
def person_follow(id):
    user = checkUser()
    friend = Friends(id = str(uuid1()),user_id = user.id,friend_id = id)
    r = make_response('''<script>alter(关注成功);history.go(-1);</script>''')
    db.session.add(friend)
    db.session.commit()
    return r

@person.route('/person/<id>',methods=['GET'])
def person_index(id):
    user = checkUser()
    person = Users.query.filter_by(id = id).all()[0]
    topics = Topic.query.filter_by(user_id = id).all()
    answers = Answer.query.filter_by(user_id = id).all()
    for a in answers:
        t = Topic.query.filter_by(id = a.topic_id).all()[0]
        a.topic_name = t.name
    return render_template(
        'person_index.html',
        user = user,
        person = person,
        topics = topics,
        answers = answers,
        base64 = base64
    )

@person.route('/person/info_update',methods=['POST'])
def person_infoupdate():
    user = checkUser()
    username = request.form.get('username')
    signature = request.form.get('signature')
    education = request.form.get('education')
    career = request.form.get('career')
    Users.query.filter_by(id = user.id).update({'name':username,'signature':signature,'education':education,'profession':career})
    db.session.commit()
    return redirect('/person/' + user.id)

@person.route('/person/image_update',methods=['POST'])
def person_imageupdate():
    user = checkUser()
    image = request.files['image'].read()
    print(image)
    Users.query.filter_by(id = user.id).update({'image':image})
    db.session.commit()
    return redirect('/person/'+user.id)