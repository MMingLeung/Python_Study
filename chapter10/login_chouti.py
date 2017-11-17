'''
http://dig.chouti.com/login

jid:ewq
password:ewq
oneMonth:1
'''

import requests
from bs4 import BeautifulSoup

r0 = requests.get('http://dig.chouti.com/')
r0_cookies_dict = r0.cookies.get_dict()
print(r0_cookies_dict)
r1 = requests.post('http://dig.chouti.com/login',
                   data={
                       "phone": "aaa",
                       "password": "bbb",
                       "oneMonth": 1,
                   },
                   cookies=r0_cookies_dict)

print(r1.text)
print(r1.cookies.get_dict())

cookie_dict={
    'gpsd':r0_cookies_dict['gpsd']
}



r2 = requests.post('http://dig.chouti.com/link/vote?linksId=15312531',
                   cookies=cookie_dict)
print(r2.text)