from tornado.web import UIModule

class Custom(UIModule):
    def render(self, *args, **kwargs):
        print(self, args, kwargs)
        # self可以获取get post传递的参数
        return 'UIModule'

    # ========= CSS 相关 =========
    def css_files(self):
        return ['/css/common.css']

    def embedded_css(self):
        tpl = """
        .c1{
            color:red
        }
        """
        return tpl

    # ========= CSS 相关 end =========

    # ========= JS 相关 =========
    def javascript_files(self):
        return ['/css/common.css']

    def embedded_javascript(self):
        tpl = """
        v = 123
        console.log(123)
        """
        return tpl
    # ========= JS 相关 end =========