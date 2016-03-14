#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     __main__.py
Author:       neilhong
@contact:     gzhongzenglin@corp.netease.com
@date:        2016-03-14 01:52:27

Description:

Changelog:

'''
import sys, signal, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request
from gevent.pywsgi import WSGIServer

from conf import config
from .models import User, Group, Base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
db = SQLAlchemy(app)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)

def run_wsgi(app):
    server = WSGIServer(
        config.SERVER_LISTEN,
        application=app
    )
    server.serve_forever()

def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

@app.route('/user', methods=['POST'])
def post_user():
    data = json.loads(request.data)
    group_info = data.get('group', None)
    group = None
    if group_info:
        group = Group(name=group_info['name'], code=group_info['code'])
        db.session.add(group)
    user = User(name=data['name'], email=data['email'], group=group)
    db.session.add(user)
    db.session.commit()
    return 'created', 204

@app.route('/user', methods=['GET'])
def get_user():
    data = db.session.query(User)
    return json.dumps([{
        'name': user.name,
        'email': user.email,
        'group': {
            'name': user.group.name,
            'code': user.group.code,
        } if user.group else None
    }for user in data])

@app.route('/group', methods=['POST'])
def post_group():
    data = json.loads(request.data)
    group = Group(name=data['name'], code=data['code'])
    db.session.add(group)
    db.session.commit()
    return 'created', 204

@app.route('/group', methods=['GET'])
def get_group():
    data = db.session.query(Group)
    return json.dumps([model_to_dict(group) for group in data])

if __name__ == '__main__':
    run_wsgi(app)
