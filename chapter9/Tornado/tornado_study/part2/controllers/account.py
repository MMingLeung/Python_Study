from tornado.web import RequestHandler
from tornado.web import authenticated

# class MattRequestHandler(RequestHandler):
#     def get_current_user(self):
#         return self.get_cookie('lalal')

class MattRequestHandler(object):
    def get_current_user(self):
        return self.get_cookie('lalal')



class LoginHandler(MattRequestHandler, RequestHandler):

    # @authenticated 只是找self.current_user
    def get(self, *args, **kwargs):
        # 反向生成url
        url1 = self.application.reverse_url('n1')

        self.render('login.html', msg="")

    def post(self, *args, **kwargs):
        # get and  post请求的参数
        # self.get_argument()
        # self.get_arguments()

        # get 请求的参数
        # slef.get_query_argument()

        user = self.get_argument('user')
        pwd = self.get_argument('pwd')
        if user =='matt' and pwd == '123':
            import time
            v = time.time() + 300
            self.set_secure_cookie('lalal', user, expires=v)
            self.redirect('/index')
        else:
            self.render('login.html', msg='账号或密码错误')

class IndexHandler(MattRequestHandler, RequestHandler):


    @authenticated
    def get(self, *args, **kwargs):
        # if not self.get_cookie('lalal'):
        #     self.redirect('/login')
        #     return None
        # self.render('index.html')
        data_list = [
            {'title':'a1', 'a':1},
            {'title':'a2', 'a':2},
            {'title':'a3', 'a':3},
        ]
        self.render('index.html', data_list=data_list)
