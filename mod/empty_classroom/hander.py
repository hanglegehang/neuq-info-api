# coding:utf-8
# Created by lihang on 2019-01-26
import json
import logging

import requests
import time
import tornado.gen
from bs4 import BeautifulSoup

from config import *
from mod.auth.hander import authApi, auth
from util.r import AESCipher


class EmptyClassroom(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        response = ''
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
            logging.info('获取学期开始' + str(int(round(time.time() * 1000))))
            r1 = s.post(INDEX_URL)
            # r2 = s.post(TERM_CHECK_URL, data={'xnm': '2018', 'xqm': '3'})
            termOption = BeautifulSoup(r1.text, 'html.parser').find(id='dm_cx')
            yearTerm = termOption.find(selected='selected').attrs['value']
            year = yearTerm.split('-')[0]
            term = yearTerm.split('-')[1]
            logging.info('获取学期结束' + str(int(round(time.time() * 1000))))

            weekParam = 0
            for i in week:
                weekParam += 2 ** (i - 1)
            dayParam = 0
            for i in day:
                dayParam += 2 ** (i - 1)
            sectionParam = 0
            for i in section:
                sectionParam += 2 ** (i - 1)
            data = {'xqh_id': '3D669E6DAB06A186E053AB14CECA64B4', 'fwzt': 'cx',
                    'xnm': year,  # 学年
                    'xqm': term,  # 学期
                    'lh': buildingNumber,  # 楼号
                    'jyfs': '0',
                    'zcd': weekParam,  # 周次
                    'xqj': dayParam,  # 星期
                    'cdlb_id': roomType,  # 教室类型
                    'jcd': sectionParam,  # 节次
                    'queryModel.showCount': '200', 'queryModel.currentPage': '1',
                    'queryModel.sortName': 'cdbh',
                    'queryModel.sortOrder': 'asc'}
            queryRes = s.post(QUERY_URL, data=data)
            parseResult = self.parser(queryRes.text)
            response = {'data': parseResult, 'code': 0, 'message': ''}
        endTime = int(round(time.time() * 1000))
        logging.info('获取空教室结束%s耗时【%s】', str(endTime), str(endTime - startTime))
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response, ensure_ascii=False))
        self.finish()

    def parser(self, text):
        result = []
        itemData = json.loads(text)
        for item in itemData['items']:
            cdjc = item['cdjc']
            jxlmc = item['jxlmc']
            lh = item['lh']
            result.append({
                'cdjc': cdjc,
                'jxlmc': jxlmc,
                'lh': lh,
            })
        return result
