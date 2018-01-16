# Web 框架知识

## 一、本质

&emsp;&emsp;WEB 框架的本质是基于 socket 编写的服务端软件。客户端是浏览器，它们的通信遵循 HTTP 协议，请求中包含请求头、请求题；响应中包含相应头、响应体。

&emsp;&emsp;服务端接受请求，分割请求头，获取请求方式、URL、参数等等作为判断依据，在路由系统中找到匹配的视图函数，进行模版渲染，返回信息给客户端。

&emsp;&emsp;客户端通过浏览器解析相应内容，展现出网站效果。

<br>

## 二、简单实现WEB框架

````python
import socket
import time
import pymysql
from jinja2 import Template


def func_1():
    '''
    处理用户请求所有信息
    :return: 用户需要的值
    '''
    f = open('login.html', 'rb')
    data = f.read()
    return data

def func_2():
    f = open('index.html', 'r')
    data = f.read()
    data = data.replace('@@tpl@@', str(time.time()))
    return data.encode('utf-8')

def func_3():
    conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db2")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 连接
    cursor.execute('select * from student')  # 游标
    data = cursor.fetchall()

    # 手动渲染
    # td_str = ''
    # for item in data:
    #     print(item[0])
    #     td_str += '<tr><td>%s</td><td>%s</td><td>%s</td><tr>' % (item[0], item[1], item[2])

    f = open('detail.html', 'r', encoding='utf-8')
    tmp_data = f.read()

    # 手动渲染
    # tmp_data = tmp_data.replace('@@tpl@@', td_str)
	
    # 通过 jinja2 渲染模版
    template = Template(tmp_data)
    data_t = template.render(detail_list=data)
    return data_t.encode('utf-8')

# 路由系统原型
routers = [
    ('/func_1', func_1),
    ('/func_2', func_2),
    ('/func_3', func_3),
]


def run():
    sock = socket.socket()
    sock.bind(('127.0.0.1', 8000))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.listen(5)
    
	# 循环监听端口号，进入阻塞
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        data_str = data.decode('utf-8')
        # 分析请求头
        headers, bodys = data_str.split('\r\n\r\n')
        temp_list = headers.split('\r\n')
        method, url, protocol = temp_list[0].split(' ')
		
        # 路由系统
        func_name = None
        for item in routers:
            if url == item[0]:
                func_name = item[1]
                break
        if func_name:
            response = func_name()
        else:
            response = b'404'
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
        conn.send(response)
        conn.close()


if __name__ == '__main__':
    run()


'''
GET / HTTP/1.1\r\n
Host: 127.0.0.1:8080\r\n
Connection: keep-alive\r\n
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36\r\n
Upgrade-Insecure-Requests: 1\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n
Accept-Encoding: gzip, deflate, br\r\n
Accept-Language: zh-CN,zh;q=0.9\r\n
Cookie: csrftoken=mbwtjOfn5JZsTFNU7tgENNCmnQbu0JMSWmXS9p6W5eBktsg4MHFVurNee2NlhPwm; sessionid=mibsrhgedsjij4v84lq52csv3qej95fj\r\n\r\n'
'''
````

<br>

### 三、HTTP 请求的生命周期

<br>

用户在浏览器输入网址 — > 通过 DNS 服务器，把网址解析成 ip:port (找到了对应服务器上的软件) —> 发送请求 

<br>

—> 服务器解析请求头信息 —> 根据 url 找到匹配的视图函数 —> 进行模版渲染 —> 返回数据给客户端 —> 客户端

<br>

浏览器对数据进行解析，显示对应页面

<br>

### 四、状态码

<br>

200：正常访问

201: 修改或新增成功

202: 成功加入队列

204: 成功删除

400: 用户请求错误

401：无权限

403: 有权限但禁止访问

404: 找不到资源

410: 资源永久删除

500: 服务器发生错误

<br>



### 五、跨域请求

<br>

&emsp;&emsp;通过浏览器访问别的域名时，因同源策略，不允许接受当前域名以外的相应信息，造成跨域问题。

<br>

##### 解决方法：基于 JSONP 规则发送与接收

&emsp;&emsp;JSONP: 客户端与服务端遵守一个规则，客户端通过 script 标签发送 GET 请求，在请求头中加入预先设定的函数名称作为参数，服务端获取该函数名，把需要返回的数据作为该函数的参数以字符串形式进行拼接，序列化后返回。那么客户端收到服务端返回的响应内容就会立即调用函数，从而获取需要的响应的内容。



形式一：script 标签



形式二：ajax

```Python
        function getU(){
            $.ajax({
                url:'http://www.jsonp_test.com:8001/users/',
                type:'GET',
                dataType:'JSONP',
                jsonp:'funcname',  // key
                jsonpCallback:'a' // value
            })}
            function a(arg) {
            console.log(arg);
        }
```



形式三：CORS 跨域资源共享

&emsp;&emsp;当前端通过 ajax 发送请求（发送一次即两次，第一次是OPTIONS，第二次是真正的），服务端先进行OPTIONS 请求中的预检，如果是 GET 简单请求直接通过，在返回对象的请求头中的 Access-Control-Allow-Origin 加入对应的客户端 IP 地址，可以实现跨域资源共享；如果是 POST 等复杂请求，需要在请求头中 Access-Control-Allow-Methods 设置允许的请求方式以及 Access-Control-Allow-Origin 地址。



