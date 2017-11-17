# 十、爬虫

# 一、基本操作

定义：根据URL，获取指定内容。

# 二、实现

## 1、requests模块

### 发送请求(本质调用request)：

1. requests.get()

2. requests.post()

3. requests.put()

### 请求中常用参数

1. url = "xx",

2. params = {'k1': 'v1', 'nid': '123'},  # GET传参数

3. cookies = {}

4. headers = {}

5. data = {}

6. json = {}

7. files 文件(filename, fileobj)

8. auth  基本验证规则。如：路由器登录页面,本质是把账号密码加密放在请求头

     def param_auth():
         from requests.auth import HTTPBasicAuth, HTTPDigestAuth
         ret = requests.get('url', auth=HTTPBasicAuth('user','pwd'))
         ret = requests.get('url', headers={'Authorization':'eqweqw'})
         return ret.text

9. timeout  float or tuple.float：等待服务器响应的时间，tuple:(连接的等待时间，等待服务器响应的时间)

10. allow_redirects  是否获取redirect页面的内容

11. proxies  代理


    	def param_proxies():
         # proxies = {
         # "http": "61.172.249.96:80",
         # "https": "http://61.185.219.126:3128",
         # }
    
         # proxies = {'http://10.20.1.128': 'http://10.10.1.10:5323'}
    
         # ret = requests.get("http://www.proxy360.cn/Proxy", proxies=proxies)
         # print(ret.headers)
    
    
         # from requests.auth import HTTPProxyAuth
         #
         # proxyDict = {
         # 'http': '77.75.105.165',
         # 'https': '77.75.105.165'
         # }
         # auth = HTTPProxyAuth('username', 'mypassword')
         #
         # r = requests.get("http://www.google.com", proxies=proxyDict, auth=auth)
         # print(r.text)


stream  流传输

         def param_stream():
             ret = requests.get('http://127.0.0.1:8000/test/', stream=True)
             print(ret.content)
             ret.close()
    
             # 自动关闭上下文
             # from contextlib import closing
            	 # with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
         		 # # 在此处理响应。
            		 # for i in r.iter_content():
            		 # print(i)

verify  https/证书携带，参数True/False

cert    证书文件 xxx.pem

session 容器，存放cookie

    def requests_session():
         import requests
    
         session = requests.Session()
    
         ### 1、首先登陆任何页面，获取cookie
    
         i1 = session.get(url="http://dig.chouti.com/help/service")
   
         ### 2、用户登陆，携带上一次的cookie，后台对cookie中的 gpsd 进行授权
         i2 = session.post(
             url="http://dig.chouti.com/login",
             data={
                 'phone': "8615131255089",
                 'password': "xxxxxx",
                 'oneMonth': ""
             }
         )
    
         i3 = session.post(
             url="http://dig.chouti.com/link/vote?linksId=8589623",
         )
         print(i3.text)

## 2.Beatuifulsoup

soup = beatifulsoup(obj.text, "html.parser")

tag_obj = soup.find()

[tag_obj,...] = soup.find_all()

tag_obj.text 获取标签内容

tag_attrs 获取属性字典

tag.get 获取标签属性