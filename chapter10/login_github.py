import requests
from bs4 import BeautifulSoup


# 1、获取token
r1 = requests.get('https://github.com/login')
s1 = BeautifulSoup(r1.text, "html.parser")
token = s1.find('input', attrs={'name': 'authenticity_token'}).get('value')
r1_cookie_dict = r1.cookies.get_dict()
print(token, r1_cookie_dict)

# 2、输入用户名密码token发送到客户端
'''
Form Data
commit:Sign in
utf8:✓
authenticity_token:mrF9105/Xb5eRLLcoMfXe2fU/QtQQ6TYDCRIPXZYb/lwLtP4+V1n2M1suEkoT2ztTenCV+FkLQ1vRhvxgZ2E+A==
login:ewq
password:qw
'''

# 发送post请求，获取cookie
r2 = requests.post("https://github.com/session",
                   data={
                       'commit': 'Sign in',
                       'utf8': '✓',
                       'authenticity_token': token,
                       'login': 'username',
                       'password': 'password'
                   },
                   cookies=r1_cookie_dict
                   )
'''
  headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                            "Referer":"https://github.com/",
                            "Host":"github.com",
                            "Origin":"https://github.com"},
                   cookies=r1_cookie_dict,
'''

r2_cookie_dict = r2.cookies.get_dict()
# print(r2.text)

# 3、新建字典保存get请求和post请求的cookie
cookie_dict = {}
cookie_dict.update(r1_cookie_dict)
cookie_dict.update(r2_cookie_dict)
print(cookie_dict)

# 4、带着cookie访问页面
r3 = requests.get(
    url = 'https://github.com/settings/emails',
    cookies = cookie_dict
)
# print(r3.text)