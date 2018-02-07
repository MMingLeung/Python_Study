#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from handlers.index import IndexHandler
from handlers.chat import OneToOneHandler, GroupHandler
from handlers.login import LoginHandler
from handlers.friends import SearchHandler, AddHandler, BlockHandler, DelGroupMemHandler, AddGroupMemHandler
from static import uimethod_index



settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'ui_modules': uimethod_index,

}

applcation = tornado.web.Application([
    (r'/index', IndexHandler),
    (r'/login', LoginHandler),
    (r'/chat_one2one', OneToOneHandler),
    (r'/search_friend', SearchHandler),
    (r'/add_friend', AddHandler),
    (r'/chat_group', GroupHandler),
    (r'/group_block', BlockHandler),
    (r'/group_del_mem', DelGroupMemHandler),
    (r'/group_add_mem', AddGroupMemHandler),

], **settings)

if __name__ == '__main__':
    applcation.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

