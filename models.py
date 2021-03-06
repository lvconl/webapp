#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : models.py
# @Author: lvconl
# @Date  : 18-2-10
#@Software : PyCharm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import datetime

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    email = db.Column(db.String(255))
    passwd = db.Column(db.String(255))
    admin = db.Column(db.Boolean(),default = False)
    name = db.Column(db.String(255))
    birth = db.Column(db.Date())
    image = db.Column(db.LargeBinary(length = 2048))
    topic_count = db.Column(db.Integer())
    answer_count = db.Column(db.Integer())
    favorite_count = db.Column(db.Integer())
    signature = db.Column(db.Text())
    profession = db.Column(db.String(100))
    education = db.Column(db.String(100))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,email,passwd,name):
        self.id = id
        self.email = email
        self.passwd = passwd
        self.name = name
        self.topic_count = 0
        self.answer_count = 0
        self.favorite_count = 0
        self.birth = datetime.date.today()
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[User] id:`{}`,admin:`{}`,email:`{}`,passwd:`{}`,name:`{}`,signature:`{}`,profession:`{}`,education:`{}`,birth:`{}`,image:`{}`,topic_count:`{}`,answer_count:`{}`,favorite_count:`{}`,created_at:`{}`".format(
            self.id,self.admin,self.email,self.passwd,self.name,self.signature,self.profession,self.education,self.birth,self.image,self.topic_count,self.answer_count,self.favorite_count,self.created_at
        )

class Topic(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    user_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    summary = db.Column(db.Text())
    content = db.Column(db.Text())
    favorite_count = db.Column(db.Integer())
    answer_count = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())

    def __init__(self,id,user_id,name,summary,content):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.summary = summary
        self.content = content
        self.favorite_count = 0
        self.answer_count = 0
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Topic] id:`{}`,user_id:`{}`,name:`{}`,summary:`{}`,content:`{}`,favorite_count:`{}`,answer_count:`{}`,created_at:`{}`".format(
            self.id,self.user_id,self.name,self.summary,self.content,self.favorite_count,self.answer_count,self.created_at
        )

class Answer(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    user_id = db.Column(db.String(255))
    topic_id = db.Column(db.String(255))
    summary = db.Column(db.Text())
    content = db.Column(db.Text())
    tag = db.Column(db.String(100))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,user_id,topic_id,content):
        self.id = id
        self.user_id = user_id
        self.topic_id = topic_id
        self.content = content
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Answer] id:`{}`,user_id:`{}`,content:`{}`,created_at:`{}`".format(
            self.id,self.user_id,self.content,self.created_at
        )

class Comments(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    answer_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    content = db.Column(db.Text())
    likeCount = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())

    def __init__(self,id,user_id,answer_id,content):
        self.id = id
        self.user_id = user_id
        self.answer_id = answer_id
        self.content = content
        self.likeCount = 0
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Content] id:`{}`,blog_id:`{}`,blog_name:`{}`,user_id:`{}`,user_name:`{}`,user_image:`{}`,content:`{}`,likeCount:`{}`,created_at:`{}`".format(
            self.id,self.blog_id,self.blog_name,self.user_id,self.user_name,self.user_image,self.content,self.likeCount,self.created_at
        )

class AnswerLikes(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    answer_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,answer_id,user_id):
        self.id = id
        self.answer_id = answer_id
        self.user_id = user_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[AnswerLikes] id:`{}`,answer_id:`{}`,user_id:`{}`,created_at:`{}`".format(
            self.id,self.answer_id,self.user_id,self.created_at
        )

class Likes(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    comment_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,comment_id,user_id):
        self.id = id
        self.comment_id = comment_id
        self.user_id = user_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Like] id:`{}`,comment_id:`{}`,user_id:`{}`,created_at:`{}`".format(
            self.id,self.comment_id,self.user_id,self.created_at
        )

class Friends(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    user_id = db.Column(db.String(255))
    friend_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,user_id,friend_id):
        self.id = id
        self.user_id = user_id
        self.friend_id = friend_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Friends] id:`{}`,user_id:`{}`,friend_id:`{}`,created_at:`{}`".format(
            self.id,self.user_id,self.friend_id,self.created_at
        )

class Favorite(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    topic_id = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())

    def __init__(self,id,topic_id,user_id):
        self.id = id
        self.topic_id = topic_id
        self.user_id = user_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return "[Favorite] id:`{}`,topic_id:`{}`,user_id:`{}`,created_at:`{}`".format(
            self.id,self.topic_id,self.user_id,self.created_at
        )