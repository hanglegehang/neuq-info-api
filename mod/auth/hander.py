# coding:utf-8
# 认证模块接口
# Created by lihang on 2017/3/22.
import json

import execjs
import requests
import time
import tornado.web
from requests import ConnectionError

from config import *
from util.r import AESCipher


class AuthHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        param = self.get_argument("p")
        response = yield tornado.gen.Task(test, param)
        self.write('NEUQ Web Service' + response)
        self.finish()

    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        crypt = AESCipher()
        deParam = crypt.decrypt(body['raw_data'])
        param = json.loads(deParam)
        username = param['card_number']
        password = param['password']
        app_key = body['app_key']
        actResult = authApi(username, password)
        actResult['app_key'] = app_key
        del actResult['cookie']
        print username + ' ' + password
        self.write(actResult)
        self.finish()

def authApi(username, password):

    result = {'code': 0, 'message': ''}
    try:
        headers = header
        s = requests.Session()
        s.headers.update(headers)
        # 访问首页
        r1= s.get(INDEX_URL, timeout=TIME_OUT)
        # 获取公钥
        r2 = s.get(PUBLIC_KEY_URL2)
        r2Json = json.loads(r2.text)
        modulus = r2Json['modulus']
        exponent = r2Json['exponent']
        # 利用公钥加密密码
        mypass = execjs.compile(open(r'sec.js').read().decode('utf-8')).call('doResult', modulus, exponent, password)
        # 登录验证
        r3 = s.post(CHECK_USER_USER, data={'yhm': username, 'mm': mypass},
                    allow_redirects=False)
        s.close()
        if r3.is_redirect:
            crypt = AESCipher()
            result['raw_data'] = crypt.encrypt(json.dumps({'card_number': 'username', 'name': '李航'}))
            result['message'] = 'ok'
            result['cookie'] = r1.headers['Set-Cookie']
        else:
            result['code'] = 401
    except requests.exceptions.ConnectTimeout:
        result['code'] = 408
        result['message'] = '请求超时'
    except ConnectionError:
        result['code'] = 400
        result['message'] = '连接错误'
    except Exception, e:
        print e
        result['code'] = 500
    return result


def test(param):
    if param == "1":
        time.sleep(5)
    return "end"
