# coding:utf-8
# Created by lihang on 2017/3/25.
import json
import requests
import tornado.gen
from config import *
from mod.auth.hander import authApi
from util.r import AESCipher


class GPAHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Herald Web Service')
        self.finish()

    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        crypt = AESCipher()
        deParam = crypt.decrypt(body['raw_data'])
        param = json.loads(deParam)
        username = param['card_number']
        password = param['password']
        app_key = body['app_key']
        checkRes = authApi(username, password)
        if checkRes['code'] == 0:
            s = requests.Session()
            headers = header
            headers['Cookie'] = checkRes['cookie']
            s.headers.update(header)
            data3 = {'xnm': '', 'xqm': '', '_search': 'false',
                     'nd': '490076975086', 'queryModel.showCount': '100',
                     'queryModel.currentPage': '1', 'queryModel.sortName': '', 'queryModel.sortOrder': 'asc',
                     'time': '1'}
            r2 = s.post(QUERY_URL2 % username, data=data3)
            retjson = {'result': self.parser(r2.text), 'card_number': username}
            # result = {'raw_data': crypt.encrypt(json.dumps(retjson)), 'code': 0, 'message': '', 'app_key': app_key}
            result = {'raw_data': retjson, 'code': 0, 'message': '', 'app_key': app_key}
            ret = json.dumps(result, ensure_ascii=False, indent=2)
            self.write(ret)
        self.finish()

    def parser(self, content):
        result = {}
        itemData = json.loads(content)
        for item in itemData['items']:
            semester = item['xnmmc']
            term = item['xqmmc']
            xqKey = semester.split('-')[0] + "0" + term
            if not result.has_key(xqKey):
                result[xqKey] = []
            result[xqKey].append({
                'course_id': item['kch'],
                'course_name': item['kcmc'],
                'score': item['cj'],
                "gpa": item['jd']
            })
        return result
