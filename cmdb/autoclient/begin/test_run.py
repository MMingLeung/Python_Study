#!coding:utf8
import subprocess

#=========获取资产信息  agent每台机器存放=========

v1 = subprocess.getoutput("ifconfig")

value1 = v1[0:30]

value2 = subprocess.getoutput("ls")


print(value1, value2)

#汇报及入库

url = "http://127.0.0.1:8000/asset.html"
import requests

response = requests.post(url, data={'k1':value1, 'k2':value2})
print(response.text)