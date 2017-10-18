# 中间件

中间件是一个类，在客户端发送请求和结束后调用这个类的相应方法。

可定义的方法：

- process_request(self,request)
- process_view(self, request, callback, callback_args, callback_kwargs)
- process_template_response(self,request,response)
- process_exception(self, request, exception)
- process_response(self, request, response)

顺序：
![](https://github.com/MMingLeung/Markdown-Picture/blob/master/%E4%B8%AD%E9%97%B4%E4%BB%B6.png?raw=true)

