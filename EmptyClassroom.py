# coding:utf-8
# Created by lihang on 2017/10/10.
import json

import execjs
import requests
data = {'yhm': '1157103','mm':'lihang133025'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
s = requests.Session()
s.headers.update(headers)
r1 = s.get('http://202.206.20.180/jwglxt/xtgl/login_slogin.html')
r2 = s.get('http://202.206.20.180/jwglxt/xtgl/login_getPublicKey.html')
r2Json = json.loads(r2.text)
modulus = r2Json["modulus"]
exponent = r2Json["exponent"]
mypass = execjs.compile(open(r"sec.js").read().decode("utf-8")).call('doResult',modulus,exponent,"lihang133025")
r3 = s.post('http://202.206.20.180/jwglxt/xtgl/login_slogin.html',data={'yhm':'1157103','mm':mypass},allow_redirects=False)
r4 = s.get('http://202.206.20.180/jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&gnmkdm=index&su=1157103')
# print r4.text
# print r3.headers
print r3.headers




