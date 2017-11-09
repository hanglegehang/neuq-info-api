# coding:utf-8
# Created by lihang on 2017/3/23.
import tornado.web
from tornado.options import define, options
from mod.library.searchhandler import LibSearchHandler
from mod.gpa.hander import GPAHandler
from mod.auth.hander import AuthHandler

define('port', default=7005, help='run on the given port', type =int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/webserv1/auth', AuthHandler),
            (r'/webserv1/gpa', GPAHandler),
            (r'/webserv1/search',LibSearchHandler)
        ]
        settings = dict(
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    Application().listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()