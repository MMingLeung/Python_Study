#! -*-coding:utf8-*-
from django.contrib.auth import authenticate
import subprocess
import random
import string
from audit import models
from django.conf import settings
from . import ssh_interactive
import datetime

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

    def token_auth(self):
        count = 0
        while count < 3:
            user_input = input("Input your token, press Enter to pass: ")
            if len(user_input) == 0:
                return
            if len(user_input) != 8:
                print('token length is incorrect!')
            else:
            # 获取token对象
                time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300) #5mins 以内
            #找出输入值等于Token.val以及创建时间大于现在时间-过期时间
                token_obj = models.Token.objects.filter(val=user_input, date__gt=time_obj).first()
                if token_obj:
                # 最新的token对象
                    if token_obj.val == user_input:
                        self.user = token_obj.account.user
                        return token_obj
            count +=1

    def start(self):
        '''
        启动交互程序
        '''
        # ############# token #############
        token_obj = self.token_auth()
        if token_obj:
            ssh_interactive.ssh_session(token_obj.host_user_bind, self.user)

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



