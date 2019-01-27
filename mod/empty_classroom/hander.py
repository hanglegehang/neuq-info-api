# coding:utf-8
# Created by lihang on 2019-01-26
import json
import logging

import requests
import time
import tornado.gen
from config import *
from mod.auth.hander import authApi, auth
from util.r import AESCipher


class EmptyClassroom(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        startTime = int(round(time.time() * 1000))
        logging.info('获取空教室开始' + str(startTime))
        username = self.get_argument("username")
        password = self.get_argument("password")
        body = json.loads(self.request.body.decode('utf-8'))
        campus = body['campus']
        week = body['week']
        day = body['day']
        roomType = body['roomType']
        section = body['section']
        buildingNumber = body['buildingNumber']
        crypt = AESCipher()
        password = crypt.decrypt(password)
        checkRes = auth(username, password)
        if checkRes['code'] == 0:
            s = requests.Session()
            headers = header
            headers['Cookie'] = checkRes['cookie']
            s.headers.update(header)
            r1 = s.post(INEX_URL % campus)
            r2 = s.post(TERM_CHECK_URL, data={'xnm': '2018', 'xqm': '3'})
            print r1.text
            print r2.text
            weekParam = 0
            for i in week:
                weekParam += 2 ** (i - 1)
            dayParam = 0
            for i in day:
                dayParam += 2 ** (i - 1)
            sectionParam = 0
            for i in section:
                sectionParam += 2 ** (i - 1)
            data = {'xqh_id': '3D669E6DAB06A186E053AB14CECA64B4', 'fwzt': 'cx', 'xnm': '2018', 'xqm': '3',
                    'lh': buildingNumber,  # 楼号
                    'jyfs': '0',
                    'zcd': weekParam,  # 周次
                    'xqj': dayParam,  # 星期
                    'cdlb_id': roomType,  # 教室类型
                    'jcd': sectionParam,  # 节次
                    'queryModel.showCount': '15', 'queryModel.currentPage': '1',
                    'queryModel.sortName': 'cdbh',
                    'queryModel.sortOrder': 'asc'}
            queryRes = s.post(QUERY_URL, data=data)
            print queryRes.text
        endTime = int(round(time.time() * 1000))
        logging.info('获取空教室结束%s耗时【%s】', str(endTime), str(endTime - startTime))

        # retjson = {'result': self.parser(r2.text), 'card_number': username}
        # result = {'raw_data': crypt.encrypt(json.dumps(retjson)), 'code': 0, 'message': ''}
        # # result = {'raw_data': retjson, 'code': 0, 'message': '', 'app_key': app_key}
        # ret = json.dumps(result, ensure_ascii=False, indent=2)
        self.write("1")
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
