#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     conftest.py
Author:       neilhong
@contact:     gzhongzenglin@corp.netease.com
@date:        2016-03-14 11:05:46

Description:

Changelog:

'''

import collections
import os
import tox

import pytest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from server import __main__ as main
from server.models import Base, User, Group

import config

DATABASE = "sqlite:////tmp/unittest.db"

DATA = collections.OrderedDict([
    (Group, [
        {
            'name': 'SA',
            'code': 'opsys.sa',
        },
        {
            'name': u'galaxy.monitor',
            'code': 'opsys.galaxy@monitor',
        },
        {
            'name': u'SAduty',
            'code': 'opsys.sa_oncall@roster',
        },
        {
            'name': 'SA',
            'code': 'h1.sa',
        },
        {
            'name': u'管理员',
            'code': u'opsys.admin@aladdin',
        },
    ]),
    (User, [
        {
            'name': 'neil',
            'email': 'neil@126.com',
        },
        {
            'name': 'neil@163.com',
            'email': 'neil@163.com',
            'group': {
                'name': '系统开发',
                'code': 'opsys.dev',
            }
        },
        {
            'name': u'neil',
            'email': u'xxxxxxxxxx@gmail.com',
        },
    ]),
])


@pytest.yield_fixture
def app(request):
    main.app.debug = True
    main.app.testing = True
    with main.app.test_request_context():
        yield main.app


@pytest.yield_fixture(scope='function')
def db(app, monkeypatch, request):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/unit_test.db'
    db = SQLAlchemy(app)
    monkeypatch.setattr(main, 'db', db)
    Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(db.engine)
    yield db

def create_group(code):
    resource = models.Group(code=code)
    resource.name = code
    resource.code = code
    return resource
