import tornado.ioloop
from part2 import uiuiui as mt
from part2 import umumum as md
from part2.controllers.account import LoginHandler, IndexHandler
import tornado.web
settings = {
    # 实际文件路径
    'template_path':'part2/tpl',
    # 实际文件路径
    'static_path':'part2/static',
    # 前缀
    'static_url_prefix':'/static/',

    'xsrf_cookies':True,
    'cookie_secret':'dqwd',
    'login_url':'/login',
    'ui_methods':mt,
    'ui_modules':md,
}

application = tornado.web.Application([
    #                           反向生成
    (r'/login', LoginHandler,{},'n1'),
    (r'/index', IndexHandler,{},'n2'),
], **settings)



if __name__ == '__main__':
    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()