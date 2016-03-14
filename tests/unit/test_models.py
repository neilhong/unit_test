#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     test_models.py
Author:       neilhong
@contact:     gzhongzenglin@corp.netease.com
@date:        2016-03-14 11:11:26

Description:

Changelog:

'''
import pytest
import json
from conftest import DATA
from code.__main__ import User, Group
from code.__main__ import get_user, get_group, post_user, post_group

def test_tox_works():
    assert 3==3

@pytest.fixture(scope='function', params=DATA[Group])
def group_data(request):
    return request.param

@pytest.fixture(scope='function', params=DATA[User])
def user_data(request):
    return request.param

class TestUser(object):
    def test_get_user(self, app, db):
        with app.test_request_context('/user', method='GET'):
            resp = get_user()
        data = json.loads(resp)
        assert isinstance(data, list)

    def test_get_group(self, app, db):
        with app.test_request_context('/group', method='GET'):
            resp = get_group()
        data = json.loads(resp)
        assert isinstance(data, list)

    def test_post_group(self, app, db, group_data):
        with app.test_request_context('/group', method='POST', data=json.dumps(group_data)):
            resp, code = post_group()
        assert isinstance(resp, basestring)
        assert code == 204

    def test_post_user(self, app, db, user_data):
        with app.test_request_context('/user', method='POST', data=json.dumps(user_data)):
            resp, code = post_user()
        assert isinstance(resp, basestring)
        assert code == 204

    @pytest.mark.parametrize('res, func', [
        ('user', 'get_user'),
        ('group', 'get_group'),
    ])
    def test_parametrize(self, app, res, func):
        with app.test_request_context('/' + res, method='get'):
            resp = eval(func)()
        data = json.loads(resp)
        assert isinstance(data, list)
