import tornado.ioloop

from part2.controllers.account import LoginHandler

settings = {
    'template_path':'tpl',
    'static_path':'static'
}

application = tornado.web.Application([
    #                           反向生成
    (r'/index', LoginHandler,{},'n1'),
], **settings)


# 模板的静态文件




# 域名匹配
# application.add_handlers('www.lala.com',[
# (r'/index', IndexHandler),
# ])



if __name__ == '__main__':
    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()