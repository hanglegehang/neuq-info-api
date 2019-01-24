# coding:utf-8
# 认证模块接口
# Created by lihang on 2017/3/22.
import json

import execjs
import requests
import time
import tornado.web
from bs4 import BeautifulSoup
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
        username = body['username']
        password = body['password']
        actResult = authApi(username, password)
        if (actResult.has_key('cookie')):
            del actResult['cookie']
        print actResult
        self.write(json.dumps(actResult, ensure_ascii=False, indent=2))
        self.finish()

def authApi(username, password):
    result = {'code': 0, 'message': ''}
    headers = header
    s = requests.Session()
    start = int(round(time.time() * 1000))
    try:
        s.headers.update(headers)
        # 访问首页
        r1 = s.get(INDEX_URL, timeout=TIME_OUT)
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
        if r3.is_redirect:
            crypt = AESCipher()
            result['data'] = {"password": crypt.encrypt(password)}
            result['message'] = 'ok'
            result['cookie'] = r1.headers['Set-Cookie']
            r4 = s.get(QUERY_INFO_URL)
            ajaxForm = BeautifulSoup(r4.text, 'html.parser').find(id='func_fields')
            studentId = ajaxForm.find(id='col_xh').find('p').string.strip()
            studentName = ajaxForm.find(id='col_xm').find('p').string.strip()
            grade = ajaxForm.find(id='col_njdm_id').find('p').string.strip()
            userType = ajaxForm.find(id='col_xslbdm').find('p').string.strip()
            profession = ajaxForm.find(id='col_zyh_id').find('p').string.strip()
            college = ajaxForm.find(id='col_jg_id').find('p').string.strip()
            result['data']['userType'] = userType
            result['data']['studentName'] = studentName
            result['data']['grade'] = grade
            result['data']['studentId'] = studentId
            result['data']['college'] = college
            result['data']['profession'] = profession
        else:
            result['code'] = 401
    except requests.exceptions.ConnectTimeout:
        result['code'] = 408
        result['message'] = '请求超时'
    except ConnectionError:
        result['code'] = 400
        result['message'] = '连接错误'
    except Exception, e:
        print Exception
        print e
        result['code'] = 500
    finally:
        s.close()
    return result

def auth(username, password):
    result = {'code': 0, 'message': ''}
    headers = header
    s = requests.Session()
    try:
        s.headers.update(headers)
        # 访问首页
        r1 = s.get(INDEX_URL, timeout=TIME_OUT)
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
        if r3.is_redirect:
            crypt = AESCipher()
            result['data'] = {"password": crypt.encrypt(password)}
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
        print Exception
        print e
        result['code'] = 500
    finally:
        s.close()
    return result


def test(param):
    if param == "1":
        time.sleep(5)
    return "end"
