#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: lvconl
# @Date  : 18-2-10
#@Software : PyCharm

class DevConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/blog'
    SECRET_KEY = 'lv1997'
    CSRF_ENABLED = True

class Config(object):
    SECRET_KEY = 'lv1997'

class ProConfig(Config):
    pass

POSTS_PER_PAGE = 3