#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-16
#@Software : PyCharm
from flask import Blueprint,session,request,redirect
from models import db,Answer,Users,Comments

from config import COOKIE_NAME

answer = Blueprint('answer',__name__,template_folder = 'templates')


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

@answer.route('/answer/delete/<id>')
def answer_delete(id):
    user = checkUser()
    if user == '':
        return redirect('/')
    a = Answer.query.filter_by(id = id).all()[0]
    print(a)
    comment = Comments.query.filter_by(answer_id = id).all()
    if len(comment):
        for c in comment:
            db.session.delete(c)
    db.session.delete(a)
    db.session.commit()
    return redirect('/person/'+user.id)