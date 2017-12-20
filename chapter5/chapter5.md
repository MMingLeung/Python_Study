# 一、软件开发规范

目录结构

Foo/

|--bin/

|    　|--foo/

|

|--foo/

|　　|---tests/

|　　|---|----__init__.py

|　　|---|----test_main.py

|　　|

|　　|--- __init__.py

|　　|---main.py

|

|

|---docs/

|　　　|----conf.py

|　　　|-----abc.rst

|

|

|--setup.py

|--requirements.txt

|-- README

---
# 二、套接字

## 1、基本概念
C/S 架构

1、硬件C/S （打印机）

2、软件C/S （web服务）


Server :
1、一直提供服务
2、绑定唯一的地址（ip+port）

互联网协议：计算机通信标准

五层协议：应用层---传输层----网络层---数据链路层---物理层

C/S物理层之间：网卡、交换机、路由器联网


数据链路层：

以太网协议--一组电信号构成一个数据包/帧 ，分成头和数据部分

head : 
定义发送者/源地址：6个字节
接受者/目标地址：6个字节
数据类型：6个字节

data：数据内容，最短46bytes,最长1500bytes

Mac地址：每块网卡拥有世界上唯一的mac地址，长度为48位2进制，通常由12位16进制表示

有了mac 地址同一网络两台主机就可以通信（通过arp协议获取另一台主机的mac 地址）

网络层：
ip地址：找到全世界独一无二的机器

例子：访问百度，通过浏览器，找到百度的子网在哪，再基于arp地址找到mac地址，定位到百度的服务器位置


传输层：
TCP/UDP
找到机器上的独一无二的软件


应用层：
应用进程

# 三、Socket

Socket 封装了TCP/UDP（在传输层和应用层之间）

套接字：AF_UNIX/AF_INET


### 1 工作流程：

基于TCP：

服务端：

获取socket()对象--->绑定IP和端口---->监听---->接受请求----->回应数据

客户端：

获取socket()对象---->建立连接------>发送请求----->获取数据------->结束

简单例子：
    #服务端
    import socket
    
    #买手机
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.SOCK_STREAM基于TCP                            
    #基于网络通信, AF_UNIX 基于文件通信
    
    #重用ip和端口
    phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #绑号码
    phone.bind(('127.0.0.1',8000))
    
    #开机 同时接收5个链接 要写在配置文件里
    phone.listen(5)
    
    while True:
    #链接循环    
    #等待电话连接    
    conn, addr = phone.accept()
        print("电话线路是",conn, "客户端的手机号是", addr)
    
        while True:
        #通讯循环        
            try: 
                #应对windows系统            
                data = conn.recv(1024)# 接受消息 最大限定 设置大了没用            
               if not data:break 
                #对于linux系统，客户端单方终端此处会一直收空            
                print("客户端发来的消息是",data)
    
                conn.send(data.upper()) 
                #send自己系统缓存，系统调用TCP/UDP协议        
            except Exception:
                break
    conn.close()
    
    phone.close()


    #客户端
    import socket
    
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    phone.connect( ( "127.0.0.1", 8000 ) )
    
    while True:
        msg = input("Please input msg: ").strip()
        if not msg:continue    
        phone.send(msg.encode('utf-8')) 
        #发到自己系统缓存    
        print("has sended ====>")
        data = phone.recv(1024) # 由操作系统收取，系统发给用户态的客户端程序                             
        print("has recv ====>")
        print(data)
    
    phone.close()

# 四、粘包
## 1、造成的原因
TCP是面向连接的、面向流的。无法得数据流的开始位置结束位置，发送端为了多个发往接收端的包，更有效发到对方，是由Nagle算法，将多次间隔时间短且数据量少的数据，合并成一个大数据块，进行封包。接收端就难以分辨其中的各个包，造成粘包，必须提供科学的拆包机制。

## 2、解决方法：封装报头
（1）固定长度

（2）包含对将要发送数据的描述信息

## 3、自定义json报头

    #仿ssh功能小程序 
    #服务器端
    import socket
    import subprocess
    import struct
    import json
    
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    phone.bind(("127.0.0.1", 8070))
    
    phone.listen(5)
    
    while True:
        conn ,addr = phone.accept()
    
        while True:
            try:
                data = conn.recv(1024)
    
                if not data:break            
                print("命令是： ", data)
                res = subprocess.Popen(data.decode("utf-8"),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                data_err = res.stderr.read()
                data_res = res.stdout.read()
    
                # if not data_err:            
                #     cmd_res =res.stdout.read()            
                # else:            
                #     cmd_res = data_err            
                #print("结果是： ", cmd_res.decode("gbk"))
                #发送报头部分            
                data_size = len(data_res)+len(data_err)
                # #i代表把数字打包成4个字节并且转成bytes            
                #conn.send(struct.pack('i', data_size))
    
                #json自定义报头            
                json_dict = {'data_size':data_size}
                head_json = json.dumps(json_dict)
                head_json_bytes = head_json.encode("utf-8")
    
                #1、先发报头长度            
                head_len = len(head_json_bytes)
                # 打包成固定长度4个字节            
                conn.send(struct.pack('i', head_len))
                #2、发报头            
                conn.send(head_json_bytes)
                #3、发送数据部分            
                conn.send(data_res)
                conn.send(data_err)
            except Exception:
                break
    
    #客户端
    import socket
    import struct
    import json
    
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    phone.connect(("192.168.0.107", 8070))
    
    while True:
        msg = input("Please input command: ").strip()
        if not msg:continue    
        phone.send(msg.encode('utf-8'))
    
        #1、收报头长度    
        head_len_struct = phone.recv(4)
        head_len = struct.unpack('i', head_len_struct)[0]
    
        #2、收报头    
        head_json_bytes = phone.recv(head_len)
        head_json = head_json_bytes.decode("utf-8")
        head_dict = json.loads(head_json)
        data_size = head_dict["data_size"]
    
        #3、收数据
        recv_size = 0    
        recv_data = b’'    
        while recv_size < data_size:
            data = phone.recv(1024)
            recv_size += len(data)
            recv_data +=data


        print(recv_data.decode("utf-8"))
---

模仿FTP小程序

    #ftp小程序
    import socket
    import struct
    import json
    import subprocess
    import os
    
    class MYTCPServer:
        address_family = socket.AF_INET
    
        socket_type = socket.SOCK_STREAM
    
        allow_reuse_address = False
        max_packet_size = 8192
        coding='utf-8'
        request_queue_size = 5
        server_dir='file_upload'
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
        def __init__(self, server_address, bind_and_activate=True):
            """Constructor.  May be extended, do not override."””   
            self.server_address=server_address
            self.socket = socket.socket(self.address_family,
                                        self.socket_type)
            if bind_and_activate:
                try:
                    self.server_bind()
                    self.server_activate()
                except:
                    self.server_close()
                    raise
                    
        def server_bind(self):
            """Called by constructor to bind the socket.        
            "”"        
            if self.allow_reuse_address:
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)
            self.server_address = self.socket.getsockname()
    
        def server_activate(self):
            """Called by constructor to activate the server.        
            "”"        
            self.socket.listen(self.request_queue_size)
    
        def server_close(self):
            """Called to clean-up the server.        
            "”"        
            self.socket.close()
    
        def get_request(self):
            """Get the request and client address from the socket.        
            "”"        
            return self.socket.accept()
    
        def close_request(self, request):
            """Called to clean up an individual request."””  
                      
            request.close()
    
        def run(self):
            while True:
                self.conn,self.client_addr=self.get_request()
                print('from client ',self.client_addr)
                while True:
                    try:
                        head_struct = self.conn.recv(4)
                        if not head_struct:break
                        head_len = struct.unpack('i', head_struct)[0]
                        head_json = self.conn.recv(head_len).decode(self.coding)
                        head_dic = json.loads(head_json)
    
                        print(head_dic)
    #head_dic={'cmd':'put','filename':'a.txt','filesize':123123}                        
                        cmd=head_dic['cmd']
                        if hasattr(self,cmd):
                            func=getattr(self,cmd)
                            func(head_dic)
                    except Exception:
                        break
                        
        def put(self,args):
            file_path=os.path.normpath(os.path.join(self.BASE_DIR,
                self.server_dir,
                args['filename']
            ))
    
            filesize=args['filesize']
            recv_size=0        
            print('----->',file_path)
            with open(file_path,'wb') as f:
                while recv_size < filesize:
                    recv_data=self.conn.recv(self.max_packet_size)
                    f.write(recv_data)
                    recv_size+=len(recv_data)
                    print('recvsize:%s filesize:%s' %(recv_size,filesize))


    tcpserver1=MYTCPServer(('127.0.0.1',8080))

    tcpserver1.run()

    import socket
    import struct
    import json
    import os


​    
    class MYTCPClient:
        address_family = socket.AF_INET
    
        socket_type = socket.SOCK_STREAM
    
        allow_reuse_address = False
        max_packet_size = 8192
        coding='utf-8'
        request_queue_size = 5
        def __init__(self, server_address, connect=True):
            self.server_address=server_address
            self.socket = socket.socket(self.address_family,
                                        self.socket_type)
            if connect:
                try:
                    self.client_connect()
                except:
                    self.client_close()
                    raise
        def client_connect(self):
            self.socket.connect(self.server_address)
    
        def client_close(self):
            self.socket.close()
    
        def run(self):
            while True:
                inp=input(">>: ").strip()
                if not inp:continue            l=inp.split()
                cmd=l[0]
                if hasattr(self,cmd):
                    func=getattr(self,cmd)
                    func(l)


        def put(self,args):
            cmd=args[0]
            filename=args[1]
            if not os.path.isfile(filename):
                print('file:%s is not exists' %filename)
                return        
           else:
                filesize=os.path.getsize(filename)
            head_dic=
    {'cmd':cmd,'filename':os.path.basename(filename),'filesize':filesize}
            print(head_dic)
            head_json=json.dumps(head_dic)
            head_json_bytes=bytes(head_json,encoding=self.coding)
    
            head_struct=struct.pack('i',len(head_json_bytes))
            self.socket.send(head_struct)
            self.socket.send(head_json_bytes)
            send_size=0        
           with open(filename,'rb') as f:
                for line in f:
                    self.socket.send(line)
                    send_size+=len(line)
                    print(send_size)
                else:
                    print('upload successful')
    
    client=MYTCPClient(('127.0.0.1',8080))
    
    client.run()

---
# 五、 基于tcp协议的socketserver
    #多线程并发
    #服务器端
    import socketserver
    
    # self.RequestHandlerClass(request, client_address, self)
    #====
    #FtpServer(conn, addr, obj)
    
    class FTPServer(socketserver.BaseRequestHandler): 
           #通信    
           def handle(self):
           print(self.request) 
           #套接字对象conn, addr        
           while True:
                data =self.request.recv(1024)
                print(data)
                self.request.send(data.upper())
    
    if __name__ == '__main__':
        obj = socketserver.ThreadingTCPServer(('127.0.0.1',8000), FTPServer)
        print(obj.server_address, obj.RequestHandlerClass, obj.socket)
        obj.serve_forever()  #链接循环 等于多个accept
    
    #客户端
    import socket
    
    phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    phone.connect( ( "127.0.0.1", 8000 ) )
    
    while True:
        msg = input("Please input msg: ").strip()
        if not msg:continue    
        phone.send(msg.encode('utf-8')) 
        #发到自己系统缓存    
        print("has sended ====>")
        data = phone.recv(1024) 
        # 由操作系统收取，系统发给用户态的客户端程序    
        print("has recv ====>")
        print(data)
    
    phone.close()

---

FTP小程序改进：

    import socketserver
    import struct
    import json
    import os


    class MyTCPServer(socketserver.BaseRequestHandler):
        max_data_size = 8192    
        coding = 'utf-8’    
        server_dir = 'file_upload’    
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
        def handle(self):
            print("From client: ", self.request)
            while True:
                try:
                    head_struct = self.request.recv(4)
                    if not head_struct:break                
                    head_len = struct.unpack('i', head_struct)[0]
                    head_json = self.request.recv(head_len).decode(self.coding)
                    head_dict = json.loads(head_json)
                    print(head_dict)
                    #head_dict = {'cmd':'put', 'filename'= 'a.txt', 'filesize':12345}
                    cmd = head_dict['cmd']
                    if hasattr(self, cmd):
                        func = getattr(self, cmd)
                        func(head_dict)
                except Exception:
                    break
        def put(self, args):
            file_path = os.path.normpath(os.path.join(self.BASE_DIR,self.server_dir,
                                                      args["filename"]))
    
            file_size = args["filesize"]
            recv_size = 0
            print("begin to write: ", file_path)
           with open(file_path, 'wb') as f:
                while recv_size < file_size:
                    data = self.request.recv(self.max_data_size)
                    f.write(data)
                    recv_size += len(data)
                    print("recvsize:%s, filesize:%s" % (recv_size, file_size))
        def get(self, args):
        cmd = args['cmd']
        filename = args['filename']
        #file_path = os.path.normpath(os.path.join('\\tmp', args["filename"]))         
        if not os.path.isfile(filename):
           print("file:%s is not exists" % filename)
           return    
        else:
           filesize = os.path.getsize(filename)
        head_dict = {'cmd':cmd, 'filename':filename, 'filesize':filesize}
        head_json_b = json.dumps(head_dict).encode(self.coding)
        head_len = len(head_json_b)
        head_struct = struct.pack('i', head_len)
        self.request.send(head_struct)
        self.request.send(head_json_b)
        send_size = 0    
       with open(filename, 'rb') as f:
           for line in f:
               self.request.send(line)
               send_size += len(line)
               print(send_size)
           else:
               print("send file successful")
    if __name__ == '__main__':
        obj = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MyTCPServer)
        obj.serve_forever()
        
    #客户端
    import socket
    import struct
    import json
    import os


​    
    class MYTCPClient:
        address_family = socket.AF_INET
    
        socket_type = socket.SOCK_STREAM
    
        allow_reuse_address = False
        max_packet_size = 8192
        coding='utf-8'
        request_queue_size = 5
        def __init__(self, server_address, connect=True):
            self.server_address=server_address
            self.socket = socket.socket(self.address_family,
                                        self.socket_type)
            if connect:
                try:
                    self.client_connect()
                except:
                    self.client_close()
                    raise
        def client_connect(self):
            self.socket.connect(self.server_address)
    
        def client_close(self):
            self.socket.close()
    
        def run(self):
            while True:
                inp=input(">>: ").strip()
                if not inp:continue            l=inp.split()
                cmd=l[0]
                if hasattr(self,cmd):
                    func=getattr(self,cmd)
                    func(l)


        def put(self,args):
            cmd=args[0]
            filename=args[1]
            if not os.path.isfile(filename):
                print('file:%s is not exists' %filename)
                return        else:
                filesize=os.path.getsize(filename)
    
            head_dic={'cmd':cmd,'filename':os.path.basename(filename),'filesize':filesize}
            print(head_dic)
            head_json=json.dumps(head_dic)
            head_json_bytes=bytes(head_json,encoding=self.coding)
    
            head_struct=struct.pack('i',len(head_json_bytes))
            self.socket.send(head_struct)
            self.socket.send(head_json_bytes)
            send_size=0        with open(filename,'rb') as f:
                for line in f:
                    self.socket.send(line)
                    send_size+=len(line)
                    print(send_size)
                else:
                    print('upload successful')


​    
​    
    client=MYTCPClient(('127.0.0.1',8080))

    client.run()
​    

---
# 六、UPD协议
UDP：用户数据报协议，无连接的，面向消息的。不会使用块的合并优化算法，由于UDP支持一对多的模式，所以接收端的skbuff（套接字缓冲区）采用了链式结构来记录每一个达到的UDP包，在每个UDP包中就有了消息头，对于接收端来说容易分区处理。
    #服务端
    import socket


    udpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpserver.bind(('127.0.0.1', 8080))
    
    while True:
    #通讯循环    
        data, addr = udpserver.recvfrom(1024)
        print(data.decode("utf-8"))
        msg = input(">>: ")
        udpserver.sendto(msg.encode("utf-8" ), addr)
    
    #客户端
    import socket
    
    udpserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpserver.bind(('127.0.0.1', 8080))
    
    while True:
    #通讯循环    
        data, addr = udpserver.recvfrom(1024)
        print(data.decode("utf-8"))
        msg = input(">>: ")
        udpserver.sendto(msg.encode("utf-8" ), addr)

# 七、进程、线程概念
## 1、操作系统的作用
操作系统位于底层硬件与应用软件之间

工作方式是==向下管理硬件，向上提供接口==

## 2、进程

一个程序在一个数据集上的一次动态执行过程。(资源管理单位（容器）)

为了实现并发，多个程序顺序执行，关键是切换，切换牵涉到状态的保存，开销非常大。


## 3、线程
一个进程可以有多个线程，使用共用的数据集，提高系统的并发性
(最小执行单位)

解决进程开销大的问题

## 4、并发
多个CPU执行多个程序叫并行

（线程ABC同时运行）

## 5、并发
一个CPU执行多个程序叫并发

（线程A执行一段时间，切换到线程B一段时间，切换到线程C一段时间，反复切换。）


## 6、串行
线程A--->线程B--->线程C

按顺序执行，必需每个线程执行完，才执行另一个线程


## 7、同步与异步
同步：一个进程在执行某个请求的时候，若请求需要一段时间才能返回信息，那么进程就一直在等待(电话)

异步：进程不需要一直等待，可以执行其他程序，当消息返回再通知原进程处理(短信)



Cpython 不能实现并行的多线程，是GIL锁导致的


## 8、threading模块
	import threading
	import time
	
	# #使用线程方式一：
	# def listen():
	#     print("listen to music”)
	#     time.sleep(3)
	#     print("listen end”)
	### def writing():
	#     print("writing article!”)
	#     time.sleep(5)
	#     print("writing end”)
	## s = time.time()
	# th1 = threading.Thread(target=listen)
	# th2 = threading.Thread(target=writing)
	## th1.start()
	# th2.start()
	## #等待线程结束，主线程再运行
	# th1.join()
	# th2.join()
	## print(time.time() - s )
	## print("end")
	#使用线程方式二：
	# class MyThread(threading.Thread):
	##     def __init__(self, num):
	#         threading.Thread.__init__(self)
	#         self.num = num
	##     def run(self):
	#         print('%s' % self.num)
	#         time.sleep(3)
	## t1 = MyThread(56)
	# t2 = MyThread(78)
	## t1.start()
	# t2.start()
	## print('end')
	
	#例子：
	import threading
	import time
	
	def listen():
	    print("listen to music")
	    print(time.ctime())
	    time.sleep(3)
	    print("listen end")
	    print(time.ctime())


	def writing():
	    print("writing article!")
	    time.sleep(5)
	    print("writing end")
	    print(time.ctime())
	
	thread = []
	th1 = threading.Thread(target=listen)
	th2 = threading.Thread(target=writing)
	
	#isAlive()：返回线程是否活动
	#getName():返回线程名
	#setName():设置线程名
	
	#threading.currentThread() 返回当前线程变量
	#threading.enumerate() 返回一个包含正在运行的线程的list
	#threading.activeCount() 返回正在运行的线程数量，等于len(threading.currentThread())
	
	thread.append(th1)
	thread.append(th2)


	if __name__ == '__main__':
	    #设置守护线程，如果主线程结束，子线程就算没有执行完也跟着结束            
	    th1.setDaemon(True)  
	    #只有一个守护线程时，主线程还需要等th2线程，程序不会结束
	    #程序直到不存在非守护线程时退出。    
	    #th2.setDaemon(True)   
	    #不用等待th2    
	    for i in thread:
	        i.start()
	        #i.join() #让线程执行完再执行主线程，从而阻塞th2线程开通
	    print("end 6666")
	    print(time.ctime())



## 8、全局解释器锁（GIL）
加在Cpython解释器上的，阻止多线程运行在统一时刻。

计算密集型：一直在使用CPU的任务，效率不如串行（没有大量切换）。

IO密集型：存在大量IO操作（socket.accept/recv），效率显著。

	#计算密集型
	import time
	def cal(n):
	    sum = 0    
	    for i in range(n):
	        sum +=i


	s = time.time()
	#开线程 慢了
	import threading
	
	th1 = threading.Thread(target=cal, args=(70000000,))
	th2 = threading.Thread(target=cal, args=(70000000,))
	print(s)
	th1.start()
	th2.start()
	
	th1.join()
	th2.join()
	
	print(time.time()-s)
	
	#不开 稍快一点
	# print(s)
	# cal(70000000)
	# cal(70000000)
	# print(time.time()-s)

python 使用多核：开多个进程，弊端是占用资源非常大，切换复杂

出路：协程，自己定义什么时候切换 + 多进程或IO多路复用

终极：换C模块实现多线程

## 9、同步锁

	#同步锁 保护用户数据
	import time
	import threading
	
	def minus_num():
	    global num
	
	    # num -=  1  
	    # Result = 0
	    #Result = 99, 因为GIL锁统一时刻只有1个线程拿到cpu权限    
	    print("准备拿锁")
	    thread_lock.acquire()
	    #获得锁 ，锁不释放时其他线程无法执行下面代码    
	    print("拿了啦")
	    temp = num
	    time.sleep(0.1) 
	    # 第一个程序运行到此处进行IO操作，GIL锁释放了，等待的时候切换到第二个程序，一直切换到最后一个线程再运行下一步    
	    #time.sleep(0.001) 
	    # 时间非常短，当下一个线程拿到的num会进行减一操作，num就会改变    
	    num = temp - 1    
	    thread_lock.release()
	    #解锁    
	    print("释放啦")
	
	num = 100
	thread_list = []
	thread_lock = threading.Lock()
	
	for i in range(100):
	    t = threading.Thread(target=minus_num)
	    t.start()
	    thread_list.append(t)
	
	for i in thread_list:
	    t.join()
	
	print("Result: ", num)

## 10、死锁和递归锁

	import threading
	import time
	
	# lock1 = threading.Lock()
	# lock2 = threading.Lock()
	#递归锁，自带计数器, 并且计数器大于一其他线程就不能获得
	Rlock = threading.RLock()
	
	class MYThread(threading.Thread):
	
	    def __init__(self):
	        threading.Thread.__init__(self)
	
	    def run(self):
	        self.fun1()
	        self.fun2()
	
	    def fun1(self):
	        '第一个程序拿到lock1、2’        
	        # lock1.acquire()        
	        Rlock.acquire()
	        print("I am %s, get lock %s----%s" %(self.name, "lock1", time.time()))
	        # lock2.acquire()        Rlock.acquire()
	        print("I am %s, get lock %s----%s" %(self.name, "lock2", time.time()))
	        # lock2.release()        Rlock.release()
	        # lock1.release()        Rlock.release()
	
	    def fun2(self):
	        # 'fun1释放后lock1,2后，其他线程竞争1锁的时候，线程1的fun2已经拿到了lock2所以继续执行’        
	        # lock2.acquire()        
	        Rlock.acquire()
	        print("I am %s, get lock %s----%s" % (self.name, "lock2", time.time()))
	        #time.sleep(0.2)#暂停一下，线程二就能拿lock1了， 然后线程二拿不到lock2， 出现死锁现象， 用递归锁解决        
	        # lock1.acquire()        
	        Rlock.acquire()
	        print("I am %s, get lock %s----%s" % (self.name, "lock1", time.time()))
	        # lock1.release()        
	        Rlock.release()
	
	        # lock2.release()        
	        Rlock.release()
	if __name__ == '__main__':
	
	    print("start",time.time())
	
	    for i in range(0, 10):
	        my_thread = MYThread()
	        my_thread.start()

## 11、协程

	#协程
	#实现并发
	import time
	
	def consumer():
	
	    r = ''    
		while True:
	
	        n = yield r
	        if not n:
	            return        
			print('[CONSUMER] << Consuming %s ..' % n)
	        time.sleep(1)
	        r = '200 OK'
	def product(c):
	
	    next(c) 
		#取值，就是运行consumer()    
		n = 0    
		while n < 5 :
	        n += 1        
			print('[PRODUCER] >> Producing %s ..'% n)
	        cr = c.send(n)
	        print('[PRODUCER Consumer retrun %s' % cr)
	    c.close()
	
	if __name__ == '__main__':
	    c = consumer()
	    product(c)


### 11.1 greenlet

	from greenlet import greenlet

	def test1():
	    print(12)
	    gr2.switch()
	    print(34)
	    gr2.switch()
	
	def test2():
	    print(56)
	    gr1.switch()
	    print(78)
	
	gr1 = greenlet(test1)
	gr2 = greenlet(test2)
	gr1.switch()

### 11.2 gevent

	#简易爬虫gevent协程的应用
	from gevent import monkey
	monkey.patch_all()
	import gevent
	from urllib import request
	import time
	
	def f(url):
	    print("GET: %s " % url)
	    resp = request.urlopen(url)
	    data = resp.read()
	    print("%d bytes received from %s "% (len(data), url))
	
	start = time.time()
	
	gevent.joinall(
	    [gevent.spawn(f, 'https://itk.org/'),
	    gevent.spawn(f, 'https://www.github.com/'),
	    gevent.spawn(f, 'https://www.zhihu.com/')],
	)
	
	print(time.time() - start)

### 11.3 event

	#event 对象： 表示某个状态
	import threading
	import time
	import logging


	logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

	def worker(event):
	    logging.debug('waiting for redis ready...')
	    while not event.isSet():
	
	        event.wait(0.1) # event状态false 线程阻塞，每间隔3s        
	        logging.debug('waiting for...')
	
	    logging.debug('redis ready, and connect to redis server and do some thing...[%s]', time.ctime())
	    time.sleep(1)
	
	def main():
	    readis_ready = threading.Event()
	    t1 = threading.Thread(target=worker, args=(readis_ready,), name='t1')
	    t1.start()
	    t2 = threading.Thread(target=worker, args=(readis_ready,), name='t2')
	    t2.start()
	
	    logging.debug('first of all, check redis server, make sure it is OK, and then trigger the redis ready event')
	    time.sleep(3)
	    readis_ready.set()#主线程设置 event为True
	if __name__ == '__main__':
	    main()

### 11.4 Process进程对象

	from multiprocessing import Process
	import os
	import time
	
	def info(name):
	
	    print("name: ", name)
	    print("parent process: ", os.getppid()) #父进程 pychram       
	    print("process id: ", os.getpid())      #当前进程    
	    print("------------------------")
	    time.sleep(1)
	
	def foo(name):
	    info(name)
	
	if __name__ == '__main__':
	    info("main process line")


	    p1 = Process(target=info, args=('matt',))
	    p2 = Process(target=foo, args=('joy',))
	    p1.start()
	    p2.start()
	
	    p1.join()
	    p2.join()
	
	    print("end.")


	from multiprocessing import Process
	import time
	
	# def f(name):
	#     print("hello", name, time.time())
	#     time.sleep(1)
	## if __name__ == '__main__’:
	#     p_list = []
	##     for i in range(3):
	#         p = Process(target=f, args=('alvin:%s' % i ,))
	#         p_list.append(p)
	#         p.start()
	#     for i in p_list:
	#         p.join()
	#     
	#并行
	#     print("end")
	
	#------多进程，对比threading.Thread快了一半------def counter():
	    i = 0    
		for i in range(70000000):
	        i = i + 1    
			return  True
	def main():
	    l = []
	    star_time = time.time()
	    for i in range(2):
	        t = Process(target=counter,)
	        t.start()
	        l.append(t)
	    for i in l:
	        i.join()
	
	    end_time = time.time() - star_time
	    print('tol time : %s' % end_time)
	
	if __name__ == '__main__':
	    main()

# 八、阻塞IO模型与非阻塞IO模型

IO模型
## 1、阻塞IO：全程阻塞
使进程不能在做其他动作，一直等到操作完成。

进程块—>recvfrom发送系统调用（用户态切换到内核态）—>（进程态）等待链接、数据（阻塞）—>复制到用户态（阻塞）—>返回给用户

	#server
	import socket
	import time
	
	sock = socket.socket()
	
	sock.bind(('127.0.0.1', 8080))
	sock.listen(5)
	
	sock.setblocking(False)#设置非阻塞
	
	while True:
	    try:
	        conn, addr = sock.accept() #阻塞等待链接
	        data = conn.recv(1024)
	        print(data.decode('utf-8'))
	    except Exception as e:
	        print(e)
	        time.sleep(3)
	
	# data = conn.recv(1024)
	#等待数据
	# print(data.decode('utf-8'))
	#将数据从内核态复制到进程中


	#client
	import socket
	
	client = socket.socket()
	client.connect(("127.0.0.1", 8080))
	
	client.send('6666666'.encode('utf8'))


## 2、非阻塞IO

进程块—>recvfrom发送系统调用（用户态切换到内核态）—>询问有无数据—>有数据就接收，没有就返回error（非阻塞） —>复制到用户态（阻塞）—>返回给用户


优点：不需要等待内核态返回数据

缺点：系统调用发送多，资源消耗大
           （数据不是实时的）


## 3、IO多路复用（监听多个连接全程阻塞）

select /poll/epoll单个进程可以同时处理多个网络连接IO ,函数不断轮训所有负责的所有socket ,当某个socket 有数据到达了，就通知用户

进程块—> select —> 发送系统调用（等于等待链接、数据） —> 接收数据 返回数据—>进程块--> recvfrom 发送系统调用 —> 复制数据(已经在内核空间) —> 复制到用户态 —> 返回给用户

	#server
	import socket
	import select
	#
	
	sock = socket.socket()
	sock.bind(('127.0.0.1', 9000))
	sock.listen(5)
	sock.setblocking(False)
	
	list = [sock,]
	
	while True:
	
	    r,w,e = select.select(list,[],[])  #原来监听一个对象，循环一次增加一个
	
	    print("wait....")
	
	    for obj in r: #1、[sock,]
	        if obj == sock:
	            conn, addr = obj.accept()
	            list.append(conn) # [sock,conn（第一个客户端发送消息产生变化）]
	
	        else:
	            try:  # 防止客户端突然中断，传来空消息，导致服务端报错
	                data = obj.recv(1024)
	                print(data.decode('utf8'))
	                send_data = input(">>: ")
	                obj.send(send_data.encode('utf8'))
	            except Exception as e:
	                list.remove(obj)
	
	            #linux 下 只需要：
	            #if not data:
	                # data = obj.recv(1024)
	                # print(data.decode('utf8'))
	                # send_data = input(">>: ")
	                # obj.send(send_data.encode('utf8'))


	#client
	import socket
	
	client = socket.socket()
	client.connect(("127.0.0.1", 9000))
	
	while True:
	    ipt = input(">>: ")
	    client.send(ipt.encode('utf8'))
	    data = client.recv(1024)
	    print(data.decode('utf8'))
	
	socket.close()


## 4、异步IO（全程无阻塞）
同步IO会引起阻塞，直到IO结束，异步IO全程无阻塞
进程块 —> 发送系统调用 —> （内核）等待链接数据、复制数据  —> 返回给用户

## 5、驱动信号


# 九、Selectors模块

select 缺点：
1、每次调用，都要把所有fd文件描述符复制到内核空间， 导致效率下降

2、遍历所有fd，查看是否有数据访问

3、最大连接数（1024）
​      

poll：最大连接数没有限制

epoll:

1、第一个函数：创建epoll句柄，一次性把fd复制到内核中

2、回调函数：某一个动作完成之后，会调用的函数为所有fd绑定回调函数，一有数据访问，触发回调函数，回调函数将fd放到链表中

3、判断链表是否为空

	import selectors # 基于select 模块实现IO多路复用
	import socket
	
	sock = socket.socket()
	sock.bind(('127.0.0.1', 9000))
	sock.listen(5)
	sock.setblocking(False)
	
	s = selectors.DefaultSelector() #根据平台选择最佳机制epoll>poll>select
	
	def accept(sock, mask):
	
	    conn, addr = sock.accept()
	    s.register(conn, selectors.EVENT_READ, read)
	
	def read(conn, mask):
	    try:
	        data = conn.recv(1024)
	        print(data.decode('utf8'))
	        send_data = input('>>: ')
	        conn.send(send_data.encode('utf8'))
	    except Exception as e:
	        s.unregister(conn)
	
	#注册，绑定sock对象和accept方法
	s.register(sock, selectors.EVENT_READ, accept)
	
	while True:
	    print('wating...')
	    events = s.select() # 监听[(key, mask), (key, mask)..]
	    for key,mask in events:
	        #print(key.data) # accept函数对象， read函数对象，
	        func = key.data
	        obj = key.fileobj
	        #print(key.fileobj) #sock， conn，
	        func(obj, mask) #accept(sock, mask), read(conn, mask)

# 十、队列(queue)

是一种数据类型，跟进程、线程有关，保证线程安全。

1、先进先出
2、先进后出

## 1、生产者消费者模型

	import queue

	que = queue.Queue(3)# 默认先进先出(FIFO)

	que.put(1)
	que.put('helo')
	#put也有阻塞状态，超出设定值就阻塞que.put('323',False)


	g = que.get()
	print(g)
	g = que.get()
	print(g)
	g = que.get()
	print(g)
	#当取不到值，处于阻塞状态
	#join()阻塞任务，直到任务完成，需要配合另一个方法task_donea = que.get()
	print(a)
	que.task_done()
	b = que.get()
	print(b)
	que.task_done()
	
	que.join()
	print('ending')


	q= queue.LifoQueue() #先进后出q.put(111)
	q.put(1112)
	q.put(1113)
	
	print(q.get())
	
	q = queue.PriorityQueue()#优先级q.put([2,'2'])
	q.put([1,'1'])
	q.put([3,'3'])
	
	print(q.get())
	
	#生产者消费者模型
	import time, random
	import queue, threading
	
	q = queue.Queue()
	
	def Producer(name):
	    count = 0   
	    while count<10:
	        print("making...")
	        time.sleep(2)
	        q.put(count)
	        print("Product %s has produced %s " % (name, count))
	        count += 1        print("Product complish.")
	
	def Consumer(name):
	    count = 0   
	    while count < 10:
	        time.sleep(1)
	        if not q.empty():
	            data = q.get()
	            print(data)
	            print("\033[32;1mConsumer %s has use %s ....\033[0m" % (name, data))
	        else:
	            print('empty')
	        count+=1
	
	p1 = threading.Thread(target=Producer, args=('A',))
	c1 = threading.Thread(target=Consumer, args=('A',))
	
	p1.start()
	c1.start()


