#!coding:utf8
import subprocess

#=========获取资产信息  agent每台机器存放=========

v1 = subprocess.getoutput("ifconfig")

value1 = v1[0:30]

value2 = subprocess.getoutput("ls")


print(value1, value2)

#=========paramiko模块中控机放一份=========
'''
远程连接服务器，执行命令，获取结果
把结果发送给api

速度慢
但无agent

软件
fabric
ansible
'''

import paramiko

#连接ssh
# ssh = paramiko.SSHClient
#
# #允许连接不在know_hosts文件的机器
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ssh.connect(hostname='c1.salt.com', port=22, username='a1', password='123')
#
# stdin, stdout, stderr = ssh.exec_command('df')
#
# result = stdout.read()







#汇报及入库

url = "http://127.0.0.1:8000/asset.html"
import requests

response = requests.post(url, data={'k1':value1, 'k2':value2})
print(response.text)

import test
print(dir(test)) #所有的变量值

for name in dir(test):
    if name.isupper():
        print(name)