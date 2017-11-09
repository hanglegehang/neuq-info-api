# coding:utf-8
# Created by lihang on 2017/3/25.
import json

import requests
import tornado.web
import tornado.gen
from config import *


class GPAHandler(tornado.web.RequestHandler):
    # @property
    # def db(self):
    #     return self.application.db
    #
    # def on_finish(self):
    #     self.db.close()

    def get(self):
        self.write('Herald Web Service')
        self.finish()
        # self.post()

    def post(self):
        username = self.get_argument('username', default=None)
        pwd = self.get_argument('password', default=None)
        status = None

        retjson = {'code': 200, 'content': ''}
        if not (username or pwd):
            retjson['code'] = 400
            retjson['content'] = 'params lack'
        else:
            data = {'yhm': username, 'mm': pwd}
            s = requests.Session()
            s.headers.update(header)
            s.get(INEX_URL)
            r1 = s.post(LOGIN_URL, data=data, allow_redirects=False)
            print r1
            if 'Location' not in r1.headers.keys():
            # if False:
                retjson['code'] = 401
            else:
                data3 = {'xnm': xnm, 'xqm': xqm, '_search': 'false',
                         'nd': '490076975086', 'queryModel.showCount': '15',
                         'queryModel.currentPage': '1', 'queryModel.sortName': '', 'queryModel.sortOrder': 'asc',
                         'time': '1'}
                r2 = s.post(QUERY_URL2 % username, data=data3)
                print r2
                retjson['content'] = self.parser(r2.text)
        ret = json.dumps(retjson, ensure_ascii=False, indent=2)
        self.write(ret)
        self.finish()

    def parser(self,content):
        items = []
        result = json.loads(content)
        for item in result['items']:
            items.append({
                'semester': item['xnmmc'],
                'term':item['xqmmc'],
                'name': item['kcmc'] ,
                'credit': item['xf'],
                'score': item['cj'],
                'type': item['ksxz'],
                'extra': item['cjbz']
            })
        return items

        # def query(username,pwd):
        #         data = {'yhm': username, 'mm': pwd}
        #         s = requests.Session()
        #         s.headers.update(header)
        #         s.get(INEX_URL)
        #         r1 = s.post(LOGIN_URL, data=data)
        #         if 'Location' not in r1.headers.keys():
        #             print "shibai"
        #         else:
        #             data3 = {'xnm': xnm, 'xqm': xqm, '_search': 'false',
        #                      'nd': '490076975086', 'queryModel.showCount': '15',
        #                      'queryModel.currentPage': '1', 'queryModel.sortName': '', 'queryModel.sortOrder': 'asc', 'time': '1'}
        #             r = s.post(QUERY_URL2 % username, data=data3)
        #             print json.dumps(parser(r.text),encoding='utf-8',ensure_ascii=False)
        # query('1157103','lihang133025')
