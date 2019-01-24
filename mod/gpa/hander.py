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
        self.post()

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        crypt = AESCipher()
        password = crypt.decrypt(password)
        # username = param['card_number']
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
            retjson = self.parser(r2.text)
            # result = {'raw_data': crypt.encrypt(json.dumps(retjson)), 'code': 0, 'message': '', 'app_key': app_key}
            result = {'data': retjson, 'code': 0, 'message': ''}
            ret = json.dumps(result, ensure_ascii=False, indent=2)
            self.write(ret)
        self.finish()

    def parser(self, content):
        result = []
        itemData = json.loads(content)
        for item in itemData['items']:
            semester = item['xnmmc']
            term = item['xqmmc']
            xqKey = semester.split('-')[0] + "0" + term
            result.append({
                'courseId': item['kch'],
                'courseName': item['kcmc'],
                'score': item['cj'],
                'credit': item['xf'],
                "gpa": item['jd'],
                "examType": item['ksxz'],
                "isExamInvalid": item['sfxwkc'],
                "semester": xqKey
            })
        return result
