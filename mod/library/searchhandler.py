# coding:utf-8
# Created by lihang on 2017/3/26.
import json
import urllib

import re
from bs4 import BeautifulSoup
import tornado.gen
from config import TIME_OUT,header
import tornado.web
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

class LibSearchHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('Herald Web Service')
        # self.finish()
        self.post()

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        data = {
            'strSearchType': self.get_argument('strSearchType'), #查询类型 title
            'match_flag': self.get_argument('match_flag'), # 匹配类型
            'historyCount': self.get_argument('historyCount'),
            'strText': self.get_argument('strText'), #查询内容
            'doctype': self.get_argument('doctype'), # 所有书刊 中文书刊
            'with_ebook': self.get_argument('with_ebook'), # 是否显示电子书刊
            'displaypg': self.get_argument('displaypg'), # 显示方式 20条 50条
            'showmode': self.get_argument('showmode'), # 显示模式
            'sort': self.get_argument('sort'), # 排序方式
            'orderby': self.get_argument('orderby'),
            'dept': self.get_argument('dept'),
        }
        retjson = {'code': 200, 'content': ''}
        try:
            client = AsyncHTTPClient()
            url='http://libopac.neuq.edu.cn/opac/openlink.php?'+urllib.urlencode(data)
            request = HTTPRequest(
                url=url,
                method='GET',
                headers=header,
                request_timeout=TIME_OUT)
            response = yield tornado.gen.Task(client.fetch, request)
            lis = BeautifulSoup(response.body,'html.parser').find(id='search_book_list').findAll('li', class_="book_list_info")
            books = []
            for li in lis:
                lit1 = li.h3.stripped_strings
                type = lit1.next()
                name = lit1.next().split('.')[1]
                index= lit1.next()
                lit2 = li.p.stripped_strings
                all= lit2.next()
                left= lit2.next()
                auther= lit2.next()
                publish= lit2.next()
                mode = re.compile(r'\d+')
                all=mode.findall(all)[0]
                left=mode.findall(left)[0]
                books.append({
                    'type': type,
                    'index': index,
                    'name': name,
                    'all': all,
                    'left': left,
                    'publish': publish,
                    'author':auther
                })
            print books
            retjson['content'] = books
        except:
            retjson['code'] = 500
            retjson['content'] = 'error'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))
        self.finish()


