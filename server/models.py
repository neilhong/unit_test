#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:     models.py
Author:       neilhong
@contact:     gzhongzenglin@corp.netease.com
@date:        2016-03-14 15:28:30

Description:

Changelog:

'''

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(128), nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', backref=backref('users', lazy='dynamic'))

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    code = Column(String(128), nullable=False)


