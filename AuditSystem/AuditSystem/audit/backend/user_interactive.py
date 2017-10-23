#! -*-coding:utf8-*-
from django.contrib.auth import authenticate

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
                host_groups = self.user.account.host_groups.all()
                for index, group in enumerate(host_groups):
                    print("%s.\t%s[%s]" % (index,
                                           group,
                                           group.host_user_binds.count()))
                print("%s.\t未分组[%s]" % (len(host_groups), self.user.account.host_user_binds.count()))
                choice = input("select group:>").strip()
                if choice.isdigit():
                    choice = int(choice)
                    host_bind_list = None
                    if choice >= 0 and choice < len(host_groups):
                        selected_group = host_groups[choice]
                        host_bind_list = selected_group.host_user_binds.all()
                    elif choice == len(host_groups):#未分组
                        host_bind_list = self.user.account.host_user_binds.all()
                    if host_bind_list:
                        while True:
                            for index, host in enumerate(host_bind_list):
                                print("%s.\t%s" % (index,
                                                   host))
                            choice2 = input("select host:>").strip()
                            if choice2.isdigit():
                                choice2 = int(choice2)
                                if choice2 >= 0 and choice2 <= len(host_bind_list):
                                    select_host = host_bind_list[choice2]
                                    print("selected host", select_host)
                            elif choice2 == 'b':
                                break



