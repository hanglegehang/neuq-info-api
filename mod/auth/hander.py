# coding:utf-8
# 认证模块接口
# Created by lihang on 2017/3/22.
import json
import execjs
import requests
import tornado.web
from requests import ConnectionError

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("NEUQ Web Service")
        self.finish()
    def post(self):
        result = authApi(self.get_argument('username'),self.get_argument('password'))
        self.write(result)
        self.finish()
        raise tornado.web.HTTPError(401)

def authApi(username, password):
        result = {'code': 200, 'content': ''}
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
            s = requests.Session()
            s.headers.update(headers)
            s.get('http://202.206.20.180/jwglxt/xtgl/login_slogin.html')
            # 获取公钥
            r2 = s.get('http://202.206.20.180/jwglxt/xtgl/login_getPublicKey.html')
            r2Json = json.loads(r2.text)
            modulus = r2Json["modulus"]
            exponent = r2Json["exponent"]
            # 利用公钥加密密码
            mypass = execjs.compile(open(r"sec.js").read().decode("utf-8")).call('doResult', modulus, exponent,password)
            # 登录验证
            r3 = s.post('http://202.206.20.180/jwglxt/xtgl/login_slogin.html', data={'yhm':username, 'mm': mypass},allow_redirects=False)
            s.close()
            if 'Location' in r3.headers.keys():
                result['content']='ok'
            else:
                result['code'] = 401
        except ConnectionError:
            result['code'] = 400
        except Exception, e:
            result['code'] = 500
        print result
        return result