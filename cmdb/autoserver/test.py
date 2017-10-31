#
# s1 = {'5', '1'}
# s2 = {'4', '5', '6'}
#
# cha = s1 - s2
# print(cha) #需要新增
#
# jiao = s1 & s2
# print(jiao) #需要更新
#
# shan = s2 - jiao - cha
# print(shan) #需要删除

# a = '23543b813530f909b477ef5ffbd3994e|1507002918.285611'
# a1,a2 = a.split('|')
# print("a1",a1)
# print("a2",a2)

import requests

requests.post(url='http://127.0.0.1:8000/api/servers/', json={'name':'matt', 'email':'matt@gmail.com'})