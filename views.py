#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-2-10
#@Software : PyCharm
from flask import render_template,make_response,request,redirect,session

from sqlalchemy import and_
from main import app
from models import db,Users,Topic,Answer,Comments,Likes
from forms import BlogTextForm,UserInfoForm,CommentForm,UpdatePasswdForm,SearchForm
from uuid import uuid1
from config import POSTS_PER_PAGE

import base64
import hashlib
import datetime
import markdown2

COOKIE_NAME = 'lvconl'

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

@app.route('/',methods = ['GET','POST'])
def index(page = 1):
    user = checkUser()
    page = request.args.get('page',1,type = int)
    pagination = Topic.query.order_by(Topic.created_at.desc()).paginate(page,per_page = POSTS_PER_PAGE,error_out = False)
    topics = pagination.items
    return render_template(
        "index.html",
        topics = topics,
        user = user,
        base64=base64,
        pagination = pagination
    )

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        users = Users.query.filter_by(email = email).all()
        if len(users) == 0:
            error = '*用户不存在'
        else:
            user = users[0]
            if user.passwd == md5(password):
                response = make_response('''<script>location.href='/';</script>''')
                if not remember is None:
                    outdate = datetime.datetime.today() + datetime.timedelta(days=30)
                    response.set_cookie(COOKIE_NAME,user.id,expires = outdate)
                    return response
                else:
                    session['id'] = user.id
                    return redirect('/')
            else:
                error = '*密码错误'
        return render_template(
            'login.html',
            error = error,
        )
    else:
        return render_template(
        'login.html'
    )

@app.route('/signout')
def signout():
    if not 'id' in session:
        response = make_response('''<script>location.href='/';</script>''')
        response.delete_cookie(COOKIE_NAME)
        return response
    else:
        session['id'] = ''
        return redirect('/')


@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template(
            'register.html'
        )
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        users = Users.query.filter_by(email = email).all()
        if len(users) > 0:
            error = '*账号已存在'
            return render_template(
                'register.html',
                error = error
            )
        passwd = md5(password)
        user = Users(id = str(uuid1()),email = email,passwd = passwd,name = name)
        try:
            db.session.add(user)
        except Exception as e:
            print(e)
        finally:
            db.session.commit()
        response = make_response('''<script>location.href='/';</script>''')
        response.set_cookie(COOKIE_NAME,user.id)
        return response
