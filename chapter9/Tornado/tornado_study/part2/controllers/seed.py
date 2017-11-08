from tornado.web import RequestHandler

class SeedHandler(RequestHandler):
    def get(self, *args, **kwargs):
        # 反向生成url
        url1 = self.application.reverse_url('n1')

        self.write("Hellow, world!")
    def post(self, *args, **kwargs):
        pass