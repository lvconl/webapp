#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-18
#@Software : PyCharm
from flask import Blueprint,render_template,session,request
from config import COOKIE_NAME
from models import Users

import base64

admin = Blueprint('admin',__name__,template_folder = 'templates')

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

@admin.route('/admin',methods=['GET'])
def admin_index():
    user = checkUser()
    return render_template(
        'admin.html',
        user = user,
        base64 = base64
    )