# AuditSystem

## 一、场景分析

1. 权限分配
	1. A用户 192.168.1.1 root
	2. B用户 192.168.1.1 mysql  
2. 主机分组功能  
3. 日志记录


## 二、系统功能简介

1. 记录用户操作
	1. 操作日志审计
2. 实现权限管理
	1. 给员工分配堡垒机账户，根据员工岗位对其堡垒机账户分配对应的登录服务器权限


## 三、系统架构

### 1、数据库设计

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/AuditSystem.png?raw=true)

### 2、功能详解

#### 1、堡垒机登录SHELL

1、入口程序audit_shell.py

实例化UserShell，调用start方法

	#! -*-coding:utf8-*-
	import sys
	import os
	
	if __name__ == '__main__':
	    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuditSystem.settings")
	    import django
	    django.setup() #手动注册django所有APP
	    from audit.backend import user_interactive
	    obj = user_interactive.UserShell(sys.argv)
	    obj.start()

2、user_interactive.py

1. 初始化基本信息
2. 用户验证
3. 选择并登录主机，切换到shell  


		class UserShell:
		    '''
		    用户登录堡垒机的shell
		    '''
		    def __init__(self, sys_argv):
		        self.sys_argv = sys_argv
		        self.user = None
		
		    def auth(self):
		        count = 0
		        while count < 3:
		            username = input('username:')
		            password = input('password:')
		            user = authenticate(username=username, password=password)
		            #None 代表认证不成功
		            #认证成功返回数据user object
		            if not user:
		                count += 1
		                print("invalid username or password!")
		            else:
		                self.user = user
		                return True
		        else:
		            print("too many attempts.")
		
		    def start(self):
		        '''
		        启动交互程序
		        '''
		        if self.auth():
		            print(self.user.account.host_user_binds.all())  # .select_related
		            while True:
		                # 获取用户组
		                host_groups = self.user.account.host_groups.all()
		                # enumerate()循环遍历，获取索引和内容
		                for index, group in enumerate(host_groups):
		                    print("%s.\t%s[%s]" % (index,
		                                           group,
		                                           group.host_user_binds.count()))
		                # 未分组的机器
		                print("%s.\t未分组[%s]" % (len(host_groups), self.user.account.host_user_binds.count()))
		                # 选择组
		                choice = input("select group:>").strip()
		                if choice.isdigit():
		                    choice = int(choice)
		                    host_bind_list = None
		                    # 选择主机记组
		                    if choice >= 0 and choice < len(host_groups):
		                        selected_group = host_groups[choice]
		                        host_bind_list = selected_group.host_user_binds.all()
		                    # 选择未分组的主机
		                    elif choice == len(host_groups):
		                        host_bind_list = self.user.account.host_user_binds.all()
		                    if host_bind_list:
		                        # 进入循环，选择主机
		                        while True:
		                            for index, host in enumerate(host_bind_list):
		                                print("%s.\t%s" % (index,
		                                                   host))
		                            choice2 = input("select host:>").strip()
		                            if choice2.isdigit():
		                                choice2 = int(choice2)
		                                if choice2 >= 0 and choice2 <= len(host_bind_list):
		                                    # 选择主机
		                                    select_host = host_bind_list[choice2]
		                                    # #################### paramiko ####################
		                                    ssh_interactive.ssh_session(select_host, self.user)
		                                    # #################### paramiko end ####################
		
		
		
		
		                                    # #################### SSH #########################
		                                    #  通过修改SSH源码增加-Z + 标识码记录用户操作      #
		                                    #   1、随机生成标识random_tag                      #
		                                    #   2、在SessionLog表创建一条记录                  #
		                                    #   3、拼接cmd命令                                 #
		                                    #   4、凭借SESSION_TRACKER_SCRIPT脚本，为其传入参数#
		                                    #   5、运行脚本，通过不断获取服务器是否有带有标识码#
		                                    #      的进程，如果有就调用strace命令              #
		                                    #   5、启动进入shell                               #
		                                    # s = string.ascii_lowercase + string.digits
		                                    # random_tag = ''.join(random.sample(s, 5))
		                                    # session_obj = models.SessionLog.objects.create(account=self.user.account, host_user_bind=select_host)
		                                    # print("selected host", select_host)
		                                    # cmd = "sshpass -p %s /usr/local/openssh/bin/ssh %s@%s -p %s -o StrictHostKeyChecking=no -Z %s" % (select_host.host_user.password,select_host.host_user.username ,select_host.host_name.ip_addr, select_host.host_name.port, random_tag)
		                                    # print(cmd)
		                                    # # 检测程序start strace and sleep1 random_tag,session_obj.id, 等待shell启动再获取进程号PID
		                                    # session_tracker_script= "%s %s %s" %(settings.SESSION_TRACKER_SCRIPT, random_tag, session_obj.id)
		                                    # session_tracker_obj = subprocess.Popen(session_tracker_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		                                    # # 切换到shell
		                                    # ssh_channel = subprocess.run(cmd, shell=True)
		                                    # print(session_tracker_obj.stdout.read(),  session_tracker_obj.stderr.read())
		                                    # #################### SSH ####################
		                            elif choice2 == 'b':
		                                break

3、（原生SSH）session_tracker.sh 脚本

	#!/bin/bash
	
	#for loop 30.get process id by random tag
	#if got the process id, start command strace
	
	for i in $(seq 1 30);do
	    echo $i $1
	    process_id=`ps -ef|grep $1 |grep -v sshpass |grep -v grep|grep -v 'session_tracker.sh' |awk '{print $2}'`
	    echo "process_id: $process_id"
	    if [ ! -z "$process_id" ];then
	        echo '###########start run strace############'
	        sudo strace -fp $process_id -t -o ssh_log/ssh_audit_$2.log;
	        break;
	    fi  
	    sleep 1  
	done;

4、（paramiko）ssh_interactive.py

源码文件demo.py -- >ssh_interactive.py
	

	import os
	import socket
	import sys
	import traceback
	from audit import models
	
	import paramiko
	try:
	    import interactive
	except ImportError:
	    from . import interactive
	
	
	
	    def manual_auth(t, username, password):
		
		    # 进行验证账号密码
		    t.auth_password(username, password)
		
		def ssh_session(bind_host_user, user_obj):
		    '''
		    传入ip 端口 主机用户对象 堡垒机用户对象
		    :param bind_host_user: 
		    :param user_obj: 
		    :return: 
		    '''
		    # ############### 登录所需信息 #################
		    hostname = bind_host_user.host_name.ip_addr
		    port = bind_host_user.host_name.port
		    username = bind_host_user.host_user.username
		    password = bind_host_user.host_user.password
		    # now connect
		    try:
		        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		        sock.connect((hostname, port))
		    except Exception as e:
		        print('*** Connect failed: ' + str(e))
		        traceback.print_exc()
		        sys.exit(1)
		
		    try:
		        t = paramiko.Transport(sock)
		        try:
		            t.start_client()
		        except paramiko.SSHException:
		            print('*** SSH negotiation failed.')
		            sys.exit(1)
		
		        try:
		            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		        except IOError:
		            try:
		                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
		            except IOError:
		                print('*** Unable to open host keys file')
		                keys = {}
		
		        # check server's host key -- this is important.
		        key = t.get_remote_server_key()
		        if hostname not in keys:
		            print('*** WARNING: Unknown host key!')
		        elif key.get_name() not in keys[hostname]:
		            print('*** WARNING: Unknown host key!')
		        elif keys[hostname][key.get_name()] != key:
		            print('*** WARNING: Host key has changed!!!')
		            sys.exit(1)
		        else:
		            print('*** Host key OK.')
		
		        if not t.is_authenticated():
		            manual_auth(t, username, password)
		        if not t.is_authenticated():
		            print('*** Authentication failed. :(')
		            t.close()
		            sys.exit(1)
		
		        chan = t.open_session()
		        chan.get_pty()
		        chan.invoke_shell()
		        print('*** Here we go!\n')
		        # ############### 进入shell ###############
		        # 数据库新增会话对象
		        session_obj = models.SessionLog.objects.create(account=user_obj.account, host_user_bind=bind_host_user)
		        interactive.interactive_shell(chan, session_obj)
		        chan.close()
		        t.close()
		
		    except Exception as e:
		        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
		        traceback.print_exc()
		        try:
		            t.close()
		        except:
		            pass
		        sys.exit(1)
	
	
5、修改堡垒机服务器上的./bashrc使用户登录堡垒机时直接运行脚本


6、图形界面


7、WEB SSH交互

shellinabox

8、图形界面上让django程序与shellinabox共享登录者信息，使登录者不必再输入堡垒机账号密码

1. 在网页上点击对应机器的按钮，自动生成token，存入数据库
2. 在shellinabox中，如果用户输入token，且跟数据库匹配，就调用登录函数
	1. token表与用户、绑定的机器关联，加上生成时间与过期时间
	2. 登录堡垒机人机交互页面，根据用户输入的token，去数据库找到对应的数据，并且判断时间是否超出过期时间（获取现在时间-过期时间， 用生成token的时间判断是否大于上述计算出来的时间，如果是则有效）


9、执行批量命令流程

1. 用户向服务器发送批量执行命令的请求
2. Django找到对应的视图函数，在函数体内启用多线程，主线程继续执行，返回一个任务id给用户，实际执行命令的函数的主线程是系统，所以django返回值后不会终止
3. 多线程获取的结果存放在数据库中
4. 用户访问获取数据的url，获取对应数据