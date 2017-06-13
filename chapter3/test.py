# NAME = 'top'
#
# def first():
#     name = 'first'
#     print(name)
#     def second():#遇到函数只编译不执行
#         name = 'second'
#         print(name)
#         def third():
#             name = 'third'
#             print(name)
#         print(name)
#         third()
#     second()
#     print(name)
#
# first() #遇到函数只编译不执行

#问路
#
# import time
#
# person_list = ['a','b','c','d']
#
# def ask_way(person_list):
#
#     if len(person_list) == 0:
#         return print('Nobody know! ')
#
#     person = person_list.pop(0)
#
#     if person == 'd':
#         return print('%s say: I know the way' %person)
#
#     time.sleep(1)
#
#     res=ask_way(person_list)
#     return res
# ask_way(person_list)

# func=lambda x:x+1
# print(func(1))
# num_l = [1,2,3,1111,333]
# def map_test(func, array):
#     ret=[]
#     for i in array:
#         res = func(i)
#         ret.append(res)
#     return ret
#
# print(map_test(lambda x:x+1,num_l))
# print(map(lambda x:x+1,num_l))
#


# res = 0
# for num in num_l:
#     res+=num

# def multi(x,y):
#     return x*y

# lambda x,y:x*y
# num_l=[1,2,3]
#
# def reduce_test(func,array):
#     res = array.pop(0)
#     for num in array:
#         res=func(res, num)
#     return res

# print(reduce_test(lambda x,y:x*y,num_l))
# from functools import reduce
# num_l = [1,2,3,4]
# print(reduce(lambda x,y:x+y,num_l))
#
# def search():
#     print('search')
#
# def add():
#     print('add')
#
# def change():
#     print('change')
#
# def delete():
#     print('delete')
#
# cmd_dic={
#     'search':search,
#     'add':add,
#     'change':change,
#     'delete':delete,
# }
#
# def tell_msg():
#     msg='''
#     search:查询
#     add：添加
#     change:更改
#     delete:删除
#     '''
#     print(msg)
#
#
# while True:
#     tell_msg()
#     choice = input('Please input your choice')
#     cmd_dic[choice]()

#闭包
#对外部作用域的引用（非全局作用域）
# x=1
# def f1():
#     x=2
#     y=1
#     def f2():
#         print(x)
#         y
#     return f2
# f=f1()
# # f()
# print(f.__closure__[0].cell_contents)
#         #闭包

#返回网页内容
#爬虫
# from urllib.request import urlopen
#
# def get(url):
#     def getpy():
#         print(urlopen(url).read())
#     return getpy
#
# f = get('http://www.python.org')
# f()

# import time
#
# def timmer(func):
#     def wrapper(*args,**kwargs):
#         #print(func)
#         start_time = time.time()
#         res = func(*args,**kwargs) #func()
#         stop_time = time.time()
#         print('run time is %s '% (stop_time-start_time))
#         return res
#     return wrapper
#
#
# @timmer #index = timmer(index)
# def index():
#     time.sleep(2)
#     print('Welcome !')
#
# @timmer
# def home(name):
#     time.sleep(2)
#     print("home %s" %name)
#
# @timmer
# def my_max(x,y):
#     print('from my_max func')
#     return x if x > y else y
#
# res = my_max(1,2) #wrapper(1,2)
# print(res)
# home('aaa') #wrapper('aaa')
#index()#timmer()运行的结果

# @timmer #auth = timmer(auth)
# def auth(name,passwd):
#     print(name,passwd)
#
# auth('aaa',123)
# current_login={'name':None, 'login':False}
#
# def auth2(auth_type):
#     def auth(func):
#         def wrapper(*args, **kwargs):
#             if current_login['name'] and current_login['login']:
#                 res = func(*args, **kwargs)
#                 return res
#             if auth_type == 'file':
#                 name = input('please name')
#                 passwd = input('please passwd')
#                 if name == 'aaa' and passwd == '123':
#                     print('Login successful')
#                     res = func(*args, **kwargs)
#                     current_login['name'] = name
#                     current_login['login'] = True
#                     return res
#                 else:
#                     print('auth error')
#             elif auth_type == 'sql':
#                 print('66666666')
#         return wrapper
#     return auth
#
# @auth2(auth_type='file') #auth2(auth_type='sql')执行，加上@auth 相当于index = auth(index)
# def index():
#     print('welcome 6666!')
#
# @auth2(auth_type='file')
# def home():
#     print('welcome home!')
# #为index函数加上认证功能
#

#
# index()
# home()
#
# @ccc
# @bbb
# @aaa
# def func():
#     pass
#
# func = ccc(bbb(aaa(func)))

# with open('user.txt','w') as f:
#     f.write(str(字典))#转换成字符串
#
# with open('user.txt','r') as f:
#     x = f.read()
#     dict = eval(x) #执行x 里面表达式，从而转换成字典


#迭代器
# l = ['a', 'b', 'c', 'd', 'e']
# i = 0
# while i< len(l):
#     print(l[i])
#     i+=1
#
# for i in range(len(l)):
#     print(l[i])

#不依赖索引，取出各个值
# d = {'a':1, 'b':2, 'c':3}
#i = d.__iter__()#有这个方法就是可迭代, 返回值就是迭代器
# print(d[i.__next__()])
# print(d[i.__next__()])
# print(d[i.__next__()])
# i = iter(d)
# while True:
#     try:
#         print(d[next(i)])
#     except StopIteration:
#         break
#
# for k in d:#for调用__iter__()方法
#     print(k)
#
# #
# i = [1,2,3]
# i =iter(i)
#
# for x in i:
#     print(x)

#生成器
#函数内包含有yield,是一个迭代器
#也就是把函数编程迭代器

#yield与return 的区别：return 执行就退出了，yield能执行多次

# def test():
#     print('helo')
#     yield 1 #等于retrun 1
#     print('www')
#     yield 2

from collections import Iterable, Iterator
# g = test()
# print(g)
# print(isinstance(g, Iterator))

# print(next(g)) #触发一个函数
# print(next(g))
#
# for i in g:
#     print(i)

# def count(n):
#     print('start !!!')
#     while n > 0:
#         yield n
#         n -=1
#     print('done')
#
# g = count(5)
#
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())


#协程函数
# def runner(func):
#     def wrapper(*args,**kwargs):
#         res = func(*args)
#         next(res)
#         return res#得到已经next一次的res
#     return wrapper
#
#
# @runner
# def eater(name):
#     print('%s start to eat ' % name)
#     food_list = []
#     while True:
#         food = yield food_list #返回值是food_list
#         print('%s get %s ,starting to eat' %(name, food))
#         food_list.append(food)
#     print('done')
#
# e = eater('Ken')
# #print(e)
#
# #print(next(e))#触发函数
# print(e.send('apple'))#为当前暂停的yield传入值
# print(e.send('watermelon'))
# print(e.send('banana'))
# print(e.send('kiwi'))

#协程爬虫
# from urllib.request import urlopen
# '''
# 传一个网址爬一次
# '''
# def runner(func):
#     def wrapper(*args,**kwargs):
#         res = func(*args)
#         next(res)
#         return res#得到已经next一次的res
#     return wrapper
#
# @runner
# def get():
#     data_web =''
#     while True:
#         url = yield data_web
#         data = urlopen(url).read()
#         print(data)
#
#
# g = get()
#
# g.send('http://www.baidu.com')
# g.send('http://www.sina.com')

#grep -r 'python' /Users/mingleung/PycharmProjects/PythonStudyLesson/day5
# import os,time
#
# def runner(func):
#     def wrapper(*args,**kwargs):
#         res = func(*args)
#         next(res)
#         return res#得到已经next一次的res
#     return wrapper
#
#
# @runner
# def search(target):
#     '找到文件的绝对路径'
#     while True:
#         dir_name = yield
#         print('start search')
#         time.sleep(3)
#         g = os.walk(dir_name)
#         for i in g:
#             #print(i[-1])  # i[-1]是文件名
#             for j in i[-1]:
#                 file_path = '%s/%s' % (i[0], j)  # 拼接
#                 target.send(file_path)#结果传给生成器target
#
# @runner
# def open_file(target):
#     '打开文件得到文件句柄'
#     while True:
#         file_path = yield
#         print('start open')
#         time.sleep(3)
#         with open(file_path,encoding="ISO-8859-1") as f:#从windows复制过来的文件需要encoding
#             target.send((file_path,f))
#
# @runner
# def read_file(target):
#     #'获取文件内容'
#     while True:
#         file_path, f= yield
#         print('start get')
#         time.sleep(3)
#         for line in f:
#             target.send((file_path,line))
#
# @runner
# def grep(pattern, target):
#     '过滤一个内容是否包含字符串python'
#     while True:
#         file_path, line = yield
#         print('start grep')
#         if pattern in line :
#             target.send(file_path)
#
# @runner
# def print_grep():
#     '打印文件路径'
#     while True:
#         file_path = yield
#         print('start print')
#         time.sleep(3)
#         print(file_path)
#
#
# g = search(open_file(read_file(grep('python',print_grep()))))
# g.send('/Users/mingleung/PycharmProjects/PythonStudyLesson/day5')

#列表生成式

#g = list_apple = ('apple%s' %i for i in range(100))
#进行for循环，结果放到list里面
#换成小括号就是生成器

#l = list(g) #list(可迭代对象)就变成列表
#print(l)


#
#l = [1,2,3,4]
# s = 'hello'
#
# list = [{i,s1} for i in l if i >2 for s1 in s ]
# print(list)

# nums_g = (i for i in range(3))
#
# print(sum(nums_g))
# money_l = []
# with open('fruit.txt') as f:
#     for line in f:
#         goods = line.split()#分割
#         res = float(goods[-1]) * float(goods[-2])
#         money_l.append(res)
# print(money_l)

#生成器表达式
# f = open('fruit.txt')
# print(sum((float(line.split()[-1]) * float(line.split()[-2]) for line in f)))

#合成生成dict
# res = []
# with open('fruit.txt') as f:
#     for line in f:
#         l = line.split()
#         dict = {'name':None,'price':None,'count':None}
#         dict['name'] = l[0]
#         dict['price'] = l[1]
#         dict['count'] = l[2]
#         res.append(dict)
#         print(res)

with open('fruit.txt') as f:
    res = (line.split() for line in f )
    money_l = ({'name':i[0],'price':i[1],'count':i[2]} for i in res if float(i[1])>1000)
    print(next(money_l))

#内置函数
abs() #绝对值
all() #传入可迭代对象，如果bool(所有值\或者空)==True，则返回True
sum() #传入可迭代对象，统计
any() #传入可迭代对象，可以为空，任何一个结果为真返回True
bin() #计算二进制
bool() #布尔值
bytes('sadsd',encoding='utf-8') #字符串转换成字节
callable() #能否被调用，返回True or False
chr(99) #数字ASCII码转换
ord('A') #字母ASCII码转换

classmethod()
staticmethod()
property()

int
    num = 1# num = int(1)
    print(type(num))
    print(num is int)#判断身份
    isinstance(num, int)#判断num是不是int类型
str #转换字符串

list # list(把可迭代对象转换成列表)

dict # d = dict(x=1,y=2,z=3)

set s= {1,2,3} #无序去重

float

bool

x = complex(1,-2j) #x.real实部 x.img虚部
tuple

frozenset

delattr
hasattr
getattr
setattr

dir() # 传入对象，查看可调用的方法

divmod() #返回元组，有两个元素x/y,x%y

enumerate([1,2,3,4]) # 迭代器，把个元素的索引和值放到元组里

eval
exec
compile
issubclass

filter
map
from functools import reduce
reduce

hash('wqewe') #得出hash值于校验文件完整性

hex #十进制转十六进制

id #身份认证

max #求最大值，可传入可迭代对象
dict_salaries={
    'a':10000,
    'b':222
}
def get_value(k):
    return  dict_salaries[k]
max(dict_salaries,key=get_value(dict_salaries))
#每一次dict_salaries给key，作为比对项，返回dict_salaries

l1 = [1,2,3]
s = 'hel'
res = zip(l1,s) #传入可迭代对象，得到zip对象，里面是元组

sorted() #返回可迭代对象组成的列表，逐个按照升序排列
sorted(l1,reverse=True) #返回可迭代对象组成的列表，逐个按照降序排列

print(sorted(get_value(l1)))

pow(3,2,2)# 3的2次方，对2取余

reversed()#反序

slice[2:5,2]#第三个元素至第六个，步长为2

vars() #没有参数返回局部名称空间=locals()

m = __import__('time')#等于import time

round(5.552223 ,6)#保留小数位数，四舍五入

#递归
'''n = 1 ,res = 10
   n > 1 ,res = age(n-1)+2
函数调用自己叫递归调用   通过栈把各个res的结果保存起来，占用内存，效率低下
用在规模未知循环次数的情景
'''
import sys
sys.setrecursionlimit(10000) #设置递归层数

def age(n):
    if n == 1:
        return 10
    else :
        return age(n-1)+2

#二分法查找
data = [1, 3, 6, 7, 9, 10, 11, 14, 18, 19, 22, 35,100]

def search(num,list):
    mid = len(list)
    if list[mid-1] == num:
        return '6666'
    elif num > list[mid-1]:
        list = list[mid:]
        return search(num,list)
    elif num < list[mid-1]:
        list = list[0:mid-1]
        return  search(num,list)

print(search(101,data))