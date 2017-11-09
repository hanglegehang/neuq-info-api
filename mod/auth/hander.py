# coding:utf-8
# 认证模块接口
# Created by lihang on 2017/3/22.
import json

import execjs
import requests
import tornado.web
from requests import ConnectionError

from config import *
from util.r import AESCipher


class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("NEUQ Web Service")
        self.finish()

    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        # print body
        # enParam = crypt.encrypt(body)
        # print enParam
        crypt = AESCipher()
        deParam = crypt.decrypt(body['raw_data'])
        param = json.loads(deParam)
        result = {'code': 0, 'message': '认证成功'}
        username = param['card_number']
        password = param['password']
        app_key = param['app_key']
        result['raw_data'] = crypt.encrypt(json.dumps({"card_number": "username", "name": "lihang"}))
        result['app_key'] = app_key
        print username + ' ' + password
        self.write(result)
        self.finish()
        raise tornado.web.HTTPError(401)


def authApi(username, password):
    result = {'code': 200, 'message': ''}
    try:
        headers = {HEADER}
        s = requests.Session()
        s.headers.update(headers)
        # 访问首页
        s.get(INDEX_URL1)
        # 获取公钥
        r2 = s.get(PUBLIC_KEY_URL2)
        r2Json = json.loads(r2.text)
        modulus = r2Json["modulus"]
        exponent = r2Json["exponent"]
        # 利用公钥加密密码
        mypass = execjs.compile(open(r"sec.js").read().decode("utf-8")).call('doResult', modulus, exponent, password)
        # 登录验证
        r3 = s.post(CHECK_USER_USER, data={'yhm': username, 'mm': mypass},
                    allow_redirects=False)
        s.close()
        if 'Location' in r3.headers.keys():
            result['content'] = 'ok'
        else:
            result['code'] = 401
    except ConnectionError:
        result['code'] = 400
    except Exception, e:
        result['code'] = 500
    print result
    return result
