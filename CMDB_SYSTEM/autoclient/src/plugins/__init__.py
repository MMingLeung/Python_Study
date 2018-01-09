#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
处理不同模式下，插件获取数据的逻辑
'''
import importlib
import traceback
from lib.conf.config import settings


class PluginManager(object):
    def __init__(self, host_name = None):
        '''
        :param host_name: ssh / saltstack 需要 
        :param plugin_dict: 插件配置字典 
        '''
        self.host_name = host_name
        self.plugin_dict = settings.PLUGINS_DICT
        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == 'ssh':
            self.ssh_user = settings.SSH_USER
            self.ssh_password = settings.SSH_PASSWORD
            self.ssh_port = settings.SSH_PORT
            self.ssh_key = settings.SSH_KEY

    def exec_plugin(self):
        '''
        获取所有的插件，并执行插件的返回值
        :return: 
        '''
        response = {}
        for key,value in self.plugin_dict.items():
            ret = {'status':True, 'data':None}
            try:
                path, class_name = value.rsplit('.',1)
                module = importlib.import_module(path)
                class_ = getattr(module, class_name)
                if hasattr(class_, 'initial'):
                    obj = class_.initial()
                else:
                    obj = class_()
                result = obj.process(self.command, self.debug)
                ret['data'] = result
            except Exception as e:
                ret['status'] = False
                ret['data'] = "[%s] [%s] 采集数据出现错误: %s" % (self.host_name if self.host_name else "Agent", class_name, traceback.format_exc())
            response[key] = ret
        return response

    def command(self, cmd):
        # 判断以哪种形式
        if self.mode == 'agent':
            return self.__agent(cmd)
        elif self.mode == 'ssh':
            return self.__ssh(cmd)
        elif self.mode == 'saltstack':
            return self.__salt(cmd)
        else:
            raise Exception('请选择正确模式')

    def __agent(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self, cmd):
        import salt.client
        # py2
        # local = salt.client.LocalClient()
        # result = local.cmd(self.host_name, 'cmd.run', [cmd])
        # return result[self.host_name]

        # py3
        import subprocess
        cmd = "salt %s cmd.run '%s'" % (self.host_name, cmd)
        output = subprocess.getoutput(cmd)
        return output

    def __ssh(self, cmd):
        import paramiko
        # key
        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.host_name, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()

        # password
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host_name, port=self.ssh_port, username=self.ssh_user, password=self.ssh_password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result


