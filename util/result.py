# coding:utf-8
# Created by lihang on 2017/11/10.


class Result:

    def __init__(self, code, message, raw_data, app_key):
        self.code = code
        self.message = message
        self.raw_data = raw_data
        self.app_key = app_key

    def __repr__(self):
        return repr((self.code, self.message, self.raw_data, self.app_key))
