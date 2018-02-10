#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import tornado.web


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from chat_room_v001.handlers.index import IndexHandler
from chat_room_v001.handlers.chat import ChatHandler


settings = {
    'template_path': 'templates',
    'static_path': 'static'
}

applcation = tornado.web.Application([
    (r'/index', IndexHandler),
    (r'/chat', ChatHandler),
], **settings)

if __name__ == '__main__':
    applcation.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

