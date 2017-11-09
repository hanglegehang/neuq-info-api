# coding:utf-8
# Created by lihang on 2017/3/23.

DB_HOST = '127.0.0.1'
DB_USER = 'herald'
DB_PWD = '******'
DB_NAME = 'herald_webservice'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' %
                       (DB_USER, DB_PWD, DB_HOST, DB_NAME), echo=False,pool_size=500, pool_recycle=100)
