#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ajax.py
# @Author: lvconl
# @Date  : 18-2-25
#@Software : PyCharm

from sqlalchemy import and_
from flask import request,session
from flask import Blueprint
from models import db,Users,Blogs,Comments,Likes
from uuid import uuid1

ajax = Blueprint('ajax',__name__)

COOKIE_NAME = 'lvconl'

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

@ajax.route('/blogs/delete')
def blog_delete():
    id = request.args.get("id")
    comments = Comments.query.filter_by(blog_id = id).all()
    blog = Blogs.query.filter_by(id = id).all()[0]
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(blog)
    db.session.commit()
    return u'删除成功！'

@ajax.route('/comment/delete')
def comment_delete():
    id = request.args.get("id")
    comment = Comments.query.filter_by(id = id).all()[0]
    db.session.delete(comment)
    db.session.commit()
    return u'删除成功!'

@ajax.route('/ajax/user/edit')
def user_edit():
    birth = request.args.get('birth')
    name = request.args.get('name')
    user = checkUser()
    Users.query.filter_by(id = user.id).update({'name':name,'birth':birth})
    db.session.commit()
    return  u'修改成功！'

@ajax.route('/ajax/comment/like')
def like_comment():
    user = checkUser()
    comment_id = request.args.get('id')
    comment = Comments.query.filter_by(id = comment_id).all()[0]
    beforeLikeCount = comment.likeCount
    afterLikeCount = beforeLikeCount + 1
    Comments.query.filter_by(id = comment_id).update({'likeCount':afterLikeCount})
    like = Likes(id = str(uuid1()),comment_id = comment_id,user_id = user.id)
    db.session.add(like)
    db.session.commit()
    return u'成功点赞'

@ajax.route('/ajax/comment/unlike')
def unlike_comment():
    user = checkUser()
    comment_id = request.args.get('id')
    comment = Comments.query.filter_by(id = comment_id).all()[0]
    beforeLikeCount = comment.likeCount
    afterLikeCount = beforeLikeCount - 1
    Comments.query.filter_by(id = comment_id).update({'likeCount':afterLikeCount})
    like = Likes.query.filter(and_(Likes.comment_id.like(comment_id),Likes.user_id.like(user.id))).all()[0]
    db.session.delete(like)
    db.session.commit()
    return u'取消点赞'