#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: lvconl
# @Date  : 18-2-11
#@Software : PyCharm
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextAreaField,FileField,RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField('name',render_kw={'placeholder': u'用户名'})
    password = PasswordField('password',validators = [DataRequired(message = u"密码不能为空"),],render_kw = {'placeholder':u'密码'})
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    name = StringField('name',render_kw = {'placeholder':'用户名'})
    email = StringField('email',render_kw = {'placeholder':'邮箱'})
    password = PasswordField('password',render_kw = {'placeholder':'密码'})
    password1 = PasswordField('password1',render_kw = {'placeholder':'重复密码'})

class BlogTextForm(FlaskForm):
    name = StringField('name',render_kw = {'placeholder':'文章标题'})
    summary = TextAreaField('summary',render_kw = {'placeHolder':'文章摘要'})
    content = TextAreaField('content',render_kw = {'placeholder':'文章内容'})
    tag = RadioField('tag',choices = [('movie',u'电影'),('technology',u'技术'),('diary',u'日记')])

class UserInfoForm(FlaskForm):
    name = StringField('name',render_kw = {'placeholder':'用户名'})
    email = StringField('email',render_kw = {'placeholder':'邮箱账号'})
    image = FileField('image',render_kw = {'placeholder':'头像'})

class CommentForm(FlaskForm):
    comment = TextAreaField('comment',render_kw = {'placeholder':'快来说两句吧...'})

class UpdatePasswdForm(FlaskForm):
    email = StringField('email',render_kw = {'placeholder':'邮箱'})
    originalPasswd = PasswordField('originalPasswd',render_kw = {'placeholder':'原密码'})
    alterPasswd = PasswordField('alterPasswd',render_kw = {'placeholder':'新密码'})
    reAlterPasswd = PasswordField('reAlterPasswd',render_kw = {'placeholder':'确认新密码'})

class SearchForm(FlaskForm):
    searchText = StringField('searchText',render_kw = {'placeholder':'搜索你感兴趣的...'})