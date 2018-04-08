#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: lvconl
# @Date  : 18-2-10
#@Software : PyCharm
from flask import render_template,make_response,request,redirect,session

from sqlalchemy import and_
from main import app
from models import db,Users,Blogs,Comments,Likes
from forms import LoginForm,RegisterForm,BlogTextForm,UserInfoForm,CommentForm,UpdatePasswdForm,SearchForm
from uuid import uuid1
from config import POSTS_PER_PAGE

import base64
import hashlib
import re
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
    pagination = Blogs.query.order_by(Blogs.created_at.desc()).paginate(page,per_page = POSTS_PER_PAGE,error_out = False)
    blogs = pagination.items
    return render_template(
        "index.html",
        blogs = blogs,
        user = user,
        base64=base64,
        pagination = pagination
    )

@app.route('/blog/<id>',methods=['GET','POST'])
def read_blog(id):
    user = checkUser()
    blogs = Blogs.query.filter_by(id = id).all()
    if len(blogs) == 0:
        blog = ''
    else:
        blog = blogs[0]
    commentResult = Comments.query.filter_by(blog_id= id).order_by(Comments.created_at.desc()).all()
    comments = []
    for c in commentResult:
        like = Likes.query.filter(and_(Likes.user_id.like(user.id),Likes.comment_id.like(c.id))).all()
        if len(like):
            c.canLike = True
        else:
            c.canLike = False
        comments.append(c)
    blog.htmlcontent = markdown2.markdown(blog.content)
    form = CommentForm()
    if request.method == 'GET':
        return render_template(
            "blog.html",
            blog = blog,
            user = user,
            comments = comments,
            base64=base64,
            form = form,
        )
    if request.method == 'POST':
        content = form.comment.data
        comment = Comments(id = str(uuid1()),blog_id = blog.id,blog_name = blog.name,user_id = user.id,user_name = user.name,user_image = user.image,content = content)
        db.session.add(comment)
        db.session.commit()
        return redirect('/blog/'+blog.id)


@app.route('/login',methods = ["GET","POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        password = request.form.get('password')
        print(password)
        remember = request.form.get('remember')
        print(remember)
        print(type(remember))
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
        print(name)
        email = request.form.get('email')
        print(email)
        password = request.form.get('password')
        print(password)
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

@app.route('/blogs/create',methods = ['GET','POST'])
def blog_create():
    user = checkUser()
    if user is None:
        return redirect('/')
    form = BlogTextForm()
    if request.method == 'GET':
        return render_template(
            'blog_edit.html',
            form = form,
            user = user,
            base64=base64
        )
    if request.method == 'POST':
        name = form.name.data
        summary = form.summary.data
        content = form.content.data
        tag = form.tag.data
        blog = Blogs(id = str(uuid1()),user_id = user.id,user_name = user.name,name = name,summary = summary,content = content,tag = tag)
        db.session.add(blog)
        db.session.commit()
        return redirect('/myblogs')

@app.route('/blogs')
def manage_blogs():
    user = checkUser()
    if user == '' or user.admin == 0:
        return redirect('/')
    page = request.args.get('page', 1, type=int)
    pagination = Blogs.query.order_by(Blogs.created_at.desc()).paginate(page, per_page=7, error_out=False)
    blogs = pagination.items
    return render_template(
        'manage_blogs.html',
        blogs = blogs,
        user = user,
        base64=base64,
        pagination = pagination
    )

@app.route('/blogs_edit/<id>',methods = ['GET','POST'])
def blog_edit(id):
    user = checkUser()
    if user == '':
        return redirect('/')
    form = BlogTextForm()
    blog = Blogs.query.filter_by(id=id).all()[0]
    if request.method == 'GET':
        form.name.data = blog.name
        form.summary.data = blog.summary
        form.content.data = blog.content
        form.tag.data = blog.tag
        return render_template(
            'blog_edit.html',
            form = form,
            base64 = base64
        )
    if request.method == 'POST':
        name = form.name.data
        summary = form.summary.data
        content = form.content.data
        tag = form.tag.data
        Blogs.query.filter_by(id = id).update({'name':name,'summary':summary,'content':content,'tag':tag})
        db.session.commit()
        return redirect('/')


@app.route('/user/edit',methods = ['GET','POST'])
def user_edit():
    user = checkUser()
    if user == '':
        return redirect('/')
    form = UserInfoForm()
    return render_template(
        'user_edit.html',
        form=form,
        user=user,
        base64=base64
    )

@app.route('/user/editImage',methods = ['GET','POST'])
def user_editImage():
    user = checkUser()
    if request.method == 'POST':
        image = request.files['image'].read()
        Users.query.filter_by(id = user.id).update({'image':image})
        Comments.query.filter_by(user_id = user.id).update({'user_image':image})
        Blogs.query.filter_by(user_id = user.id).update({'user_image':image})
        db.session.commit()
        return redirect('/')

@app.route('/user/<id>')
def user(id):
    user = checkUser()
    user_info = Users.query.filter_by(id = id).all()[0]
    user_blog = Blogs.query.filter_by(user_id = id).order_by(Blogs.created_at.desc()).limit(2).all()
    user_comment = Comments.query.filter_by(user_id = id).order_by(Comments.created_at.desc()).limit(2).all()
    form = UserInfoForm()
    return render_template(
        'user_index.html',
        user = user,
        user_info = user_info,
        user_blog = user_blog,
        user_comment = user_comment,
        base64 = base64,
        form = form
    )

@app.route('/updatepasswd',methods = ['GET','POST'])
def updatepasswd():
    user = checkUser()
    if user == '':
        return redirect('/')
    form = UpdatePasswdForm()
    if request.method == 'GET':
        return render_template(
            'updatepasswd.html',
            user = user,
            base64 = base64,
            form = form
        )
    if request.method == 'POST':
        email = form.email.data
        originalPasswd = form.originalPasswd.data
        alterPasswd = form.alterPasswd.data
        reAlterPasswd = form.reAlterPasswd.data
        if not email == user.email:
            error = '邮箱错误'
            return render_template(
                'updatepasswd.html',
                user=user,
                base64=base64,
                form=form,
                error = error
            )
        if not md5(originalPasswd) == user.passwd:
            error = '原密码错误'
            return render_template(
                'updatepasswd.html',
                user=user,
                base64=base64,
                form=form,
                error = error
            )
        if alterPasswd != reAlterPasswd:
            error = '两次输入密码不一致'
            return render_template(
                'updatepasswd.html',
                user=user,
                base64=base64,
                form=form,
                error = error
            )
        Users.query.filter_by(id = user.id).update({'passwd':md5(alterPasswd)})
        db.session.commit()
        signout()
        return redirect('/')

@app.route('/myblogs',methods = ['GET','POST'])
def myblogs(page = 1):
    user = checkUser()
    if user == '':
        return redirect('/')
    page = request.args.get('page', 1, type=int)
    pagination = Blogs.query.filter_by(user_id = user.id).order_by(Blogs.created_at.desc()).paginate(page, per_page=5, error_out=False)
    blogs = pagination.items
    return render_template(
        'person_blog.html',
        user=user,
        base64 = base64,
        blogs = blogs,
        pagination = pagination
    )

@app.route('/mycomments',methods = ['GET','POST'])
def mycomments(page = 1):
    user = checkUser()
    if user == '':
        return redirect('/')
    page = request.args.get('page',1,type = int)
    pagination = Comments.query.filter_by(user_id = user.id).order_by(Comments.created_at.desc()).paginate(page,per_page = 6,error_out = False)
    comments = pagination.items
    return render_template(
        'person_comment.html',
        base64 = base64,
        comments = comments,
        user = user,
        pagination = pagination
    )

@app.route('/comment/<id>',methods = ['GET','POST'])
def delete_comment(id):
    user = checkUser()
    if user == '':
        return redirect('/')
    comment = Comments.query.filter_by(id = id).all()[0]
    blod_id = comment.blog_id
    db.session.delete(comment)
    db.session.commit()
    if request.method == 'POST':
        return redirect('/mycomments')
    else:
        return redirect('/blog/'+blod_id)

@app.route('/search',methods = ['GET','POST'])
def search():
    user = checkUser()
    form = SearchForm()
    if request.method == 'GET' or form.searchText.data is '':
        return render_template(
            'search.html',
            user = user,
            base64 = base64,
            form = form
        )
    else:
        text = form.searchText.data
        searchText = '%' + text + '%'
        blogsBaseName = Blogs.query.filter(Blogs.name.ilike(searchText)).all()
        blogsBaseSummary = Blogs.query.filter(Blogs.summary.ilike(searchText)).all()
        blogs = blogsBaseName + blogsBaseSummary
        return render_template(
            'search.html',
            user=user,
            base64=base64,
            form=form,
            blogs = blogs,
            text = text
        )

@app.route('/users')
def manage_users(page = 1):
    user = checkUser()
    if user is '' or user.admin == 0:
        return redirect('/')
    page = request.args.get('page',1,type = int)
    pagination = Users.query.paginate(page,per_page = 6,error_out = False)
    manaUser = pagination.items
    return render_template(
        'manage_users.html',
        user = user,
        manaUser = manaUser,
        base64 = base64,
        pagination = pagination
    )

@app.route('/delete/user/<id>')
def delete_user(id):
    user = checkUser()
    if user.admin == 0:
        return redirect('/')
    u = Users.query.filter_by(id = id).all()[0]
    blogs = Blogs.query.filter_by(user_id = u.id).all()
    comments = Comments.query.filter_by(user_id = u.id).all()
    for blog in  blogs:
        db.session.delete(blog)
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(u)
    db.session.commit()
    return redirect('/users')

@app.route('/updateToAdmin/<user_id>')
def updateToAdmin(user_id):
    user = checkUser()
    if user is None or user.admin == 0:
        return redirect('/')
    Users.query.filter_by(id = user_id).update({'admin':1})
    db.session.commit()
    r = make_response('''<script>alert('设置成功!');location.href = '/users';</script>''')
    return r

@app.route('/tag/movie')
def movie(page = 1):
    user = checkUser()
    page = request.args.get('page', 1, type=int)
    pagination = Blogs.query.filter_by(tag = 'movie').order_by(Blogs.created_at.desc()).paginate(page, per_page=POSTS_PER_PAGE, error_out=False)
    blogs = pagination.items
    return render_template(
        "index.html",
        blogs=blogs,
        user=user,
        base64=base64,
        pagination=pagination
    )

@app.route('/tag/technology')
def technology(page = 1):
    user = checkUser()
    page = request.args.get('page', 1, type=int)
    pagination = Blogs.query.filter_by(tag = 'technology').order_by(Blogs.created_at.desc()).paginate(page,
                                                                                               per_page=POSTS_PER_PAGE,
                                                                                               error_out=False)
    blogs = pagination.items
    return render_template(
        "index.html",
        blogs=blogs,
        user=user,
        base64=base64,
        pagination=pagination
    )

@app.route('/tag/diary')
def diary(page = 1):
    user = checkUser()
    page = request.args.get('page', 1, type=int)
    pagination = Blogs.query.filter_by(tag = 'diary').order_by(Blogs.created_at.desc()).paginate(page,
                                                                                                    per_page=POSTS_PER_PAGE,
                                                                                                    error_out=False)
    blogs = pagination.items
    return render_template(
        "index.html",
        blogs=blogs,
        user=user,
        base64=base64,
        pagination=pagination
    )