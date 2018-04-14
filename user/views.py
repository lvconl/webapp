#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-4-14
#@Software : PyCharm
from flask import Blueprint,request

person = Blueprint('person',__name__,template_folder = 'templates')

@person.route('/person/follow')
def person_follow():
    id = request.args.get('id')
    print(id)
    return u'获取成功'