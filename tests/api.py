#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     test.py
Author:       neilhong
@contact:     gzhongzenglin@corp.netease.com
@date:        2016-03-14 03:08:09

Description:

Changelog:

'''

import requests
import sys
import pprint

URL = 'http://192.168.56.190:10000'
headers = {}

def parse(r):
    code = int(r.status_code)
    if code >= 200 and code <= 201:
        if isinstance(r.text, basestring):
            return r.text
        result = json.loads(r.text)
        #pprint(result);
        return result
    else:
        print r.status_code, r.text

def post(url, data=None):
    url = URL + url
    r = requests.post(url, json=data, headers=headers)
    return parse(r)

def put(url, data=None):
    url = URL + url
    r = requests.put(url, json=data, headers=headers)
    return parse(r)

def get(url, params=None):
    url = URL + url
    r = requests.get(url, params=params, headers=headers)
    return parse(r)

def delete(url):
    url = URL + url
    r = requests.delete(url, headers=headers)
    return parse(r)

def post_group():
    data = {
        'name': '测试组',
        'code': 'qa'
    }
    url = '/group'
    pprint(post(url, data))

def post_user():
    data = {
        'name': '洪增林',
        'email': 'test@163.com',
        'group': {
            'name': '程序',
            'code': 'dev',
        }
    }
    url = '/user'
    pprint(post(url, data))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        eval(cmd)(*sys.argv[2:])
    else:
        get_users()
