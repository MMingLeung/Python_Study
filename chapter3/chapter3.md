# 一、函数

为何要用函数：解决代码重用问题、统一维护、程序的组织结构清晰，可读性强

## 1、定义

        def test(x):
            '''注释'''
            代码
            return res 

## 2、运行

    test()

函数名代表内存地址   （传入参数,或者填写默认参数）

*args(接受多个参数换成元祖)

**kwargs(接受多个参数换成字典形式)

## 3、全局变量、局部变量

全局变量：定格定义，任何位置都能调用

                函数内global XXX 修改全局变量

局部变量：在函数内定义的


    NAME = 'top'
    
    def first():
        name = 'first'
        print(name)
        def second():#遇到函数只编译不执行
            name = 'second'
            print(name)
            def third():
                name = 'third'
                print(name)
            print(name)
            third()
        second()
        print(name)
    
    first() #遇到函数只编译不执行


## 4、函数递归

需要有明确的结束条件return

    #无限循环
    def calc(n):
         print(n)
         calc(n)
    
    calc(10)

## 5、作用域和命名空间

内置命名空间

                                  全局作用域
全局命名空间

                                  局部作用域

局部命名空间

## 6、函数对象与闭包
 
    #模块化
    def search():
        print('search')
    
    def add():
        print('add')
    
    def change():
        print('change')
    
    def delete():
        print('delete')
    
    cmd_dic={
        'search':search,
        'add':add,
        'change':change,
        'delete':delete,
    }
    
    def tell_msg():
        msg='''
        search:查询
        add：添加
        change:更改
        delete:删除
        '''
        print(msg)
    
    while True:
        tell_msg()
        choice = input('Please input your choice')
        cmd_dic[choice]()




    #闭包
    #对外部作用域的引用（非全局作用域）
    x=1
    def f1():
        x=2
        y=1
        def f2():
            print(x)
            y
        return f2
    f=f1()
    # f()
    print(f.__closure__[0].cell_contents)
    
    #返回网页内容
    #爬虫
    from urllib.request import urlopen
    
    def get(url):
        def getpy():
            print(urlopen(url).read())
        return getpy
    
    f = get('http://www.python.org')
    f()

## 7、装饰器及开放封闭原则
不修改被装饰函数的代码

（1）无参装饰器

    import time
    
    def timmer(func):
        def wrapper(*args,**kwargs):
            #print(func)
            start_time = time.time()
            func(*args,**kwargs) #home(name)
            stop_time = time.time()
            print('run time is %s '% (stop_time-start_time))
        return wrapper
    
    @timmer #index = timmer(index)
    def index():
        time.sleep(2)
        print('Welcome !')
    
    @timmer
    def home(name):
        time.sleep(2)
        print("home %s" %name)
    
    def my_max(x,y):
        print('from my_max func')
        return x+y
    
    # home('aaa') #wrapper('aaa')
    #index()#timmer()运行的结果
    
    @timmer #auth = timmer(auth)
    def auth(name,passwd):
        print(name,passwd)
    
    auth('aaa',123)

（2）有参装饰器

    #为index函数加上认证功能
    current_login={'name':None, 'login':False}
    
    def auth2(auth_type):
        def auth(func):
            def wrapper(*args, **kwargs):
                if current_login['name'] and current_login['login']:
                    res = func(*args, **kwargs)
                    return res
                if auth_type == 'file':
                    name = input('please name')
                    passwd = input('please passwd')
                    if name == 'aaa' and passwd == '123':
                        print('Login successful')
                        res = func(*args, **kwargs)
                        current_login['name'] = name
                        current_login['login'] = True
                        return res
                    else:
                        print('auth error')
                elif auth_type == 'sql':
                    print('66666666')
            return wrapper
        return auth
    
    @auth2(auth_type='file') #auth2(auth_type='sql')执行，加上@auth 相当于index = auth(index)
    def index():
        print('welcome 6666!')
    
    @auth2(auth_type='file')
    def home():
        print('welcome home!')




    #多个装饰器
    @ccc
    @bbb
    @aaa
    def func():
        pass
    func = ccc(bbb(aaa(func)))
    #print XXX.__doc__打印帮助信息
    import functools import wraps
    @wraps(func)

## 8、迭代器和生成器、协成函数

有__iter__方法的都是可迭代的对象

迭代器：对象.__iter__()得到的结果是迭代器

特性：迭代器.__next__() 取下一个值
           
优点：1、 提供统一的迭代对象的方式，不依赖于索引
           2、惰性计算

缺点：1、无法获取迭代器长度
           2、一次性的，只能往后取值，不能取某个位置的值

           
（1）迭代器

#优点：不依赖索引，取出各个值(字典，集合，文件)，节省内存，惰性计算特性
#缺点：1、无法获取迭代器长度，不如list索引取值灵活。
      2、一次性，只能往后取值

    d = {'a':1, 'b':2, 'c':3}
    #i = d.__iter__()#有这个方法就是可迭代, 返回值就是迭代器
    #print(d[i.__next__()])
    #print(d[i.__next__()])
    #print(d[i.__next__()])
    i = iter(d)
    while True:
        try:
            print(next(i))
        except StopIteration:
            break
    
    i = [1,2,3]
    i =iter(i)
    
    for x in i:
        print(x)

    from collections import Iterable, Iterator
         isinstance(i, Iterable)
    #判断i是否可迭代
    #有__iter__方法就是可迭代
    #有__next___方法就是迭代器

（2）生成器
函数带有yield的就是生成器，本质是迭代器

yield 把__iter__ __next__方法封装到函数内部

#生成器
#函数内包含有yield,是一个迭代器
#也就是把函数编程迭代器


#yield与return 的区别：return 执行就退出了，yield能执行多次
                      yield保存函数本次运行的状态

    def test():
        print('helo')
        yield 1 #等于retrun 1
        print('www')
        yield 2

    from collections import Iterable, Iterator
    g = test()
    # print(g)
    # print(isinstance(g, Iterator))
    
    # print(next(g)) #触发一个函数
    # print(next(g))
    
    for i in g:
        print(i)
    
    # def count(n):
    #     print('start !!!’)
    #     while n > 0:
    #         yield n
    #         n -=1
    #     print('done’)
    ## g = count(5)
    ## print(g.__next__())
    # print(g.__next__())
    # print(g.__next__())
    # print(g.__next__())
    # print(g.__next__())
    
    def eater(name):
        print('%s start to eat ' % name)
        food_list = []
        while True:
            food = yield food_list #返回值是food_list
            print('%s get %s ,starting to eat' %(name, food))
            food_list.append(food)
    
        print('done')
    
    e = eater('Ken')
    #print(e)
    print(next(e))#触发函数
    print(e.send('apple'))#为当前暂停的yield传入值
    print(e.send('watermelon'))
    print(e.send('banana'))
    print(e.send('kiwi'))

    #协程爬虫
    from urllib.request import urlopen
    '''
    传一个网址爬一次
    '''
    def runner(func):
        def wrapper(*args,**kwargs):
            res = func(*args)
            next(res)
            return res#得到已经next一次的res
        return wrapper
    
    @runner
    def get():
        data_web =''
        while True:
            url = yield data_web
            data = urlopen(url).read()
            print(data)
    
    g = get()
    
    g.send('http://www.baidu.com')
    g.send('http://www.sina.com')




## 6、匿名函数

func=lambda x:x+1

形参：结果

print(func(1))



## 7、声明式编程

（1）列表生成式

###把中括号换成小括号就是生成器###

():省内存
[]:占内存

    list = ['apple%s' %i for i in range(100)]#最后可以加if判断


    #进行for循环，结果放到list里面
    
    g = list_apple = ('apple%s' %i for i in range(100))
    l = list(g) #list(可迭代对象)就变成列表
    print(l)

    l = [1,2,3,4]
    s = 'hello'
    list = [{i,s1} for i in l if i >2 for s1 in s ]
    print(list)
    #如果i>2 再拼接

（2）生成器表达式

    l = list(g) #list(可迭代对象)就变成列表
    print(l)
    
    f = open('fruit.txt')
    g = (float(line.split()[-1]) * float(line.split()[-2]) for line in f)
    print(sum(g))

    #合成生成dict
    res = []
    with open('fruit.txt') as f:
        for line in f:
            l = line.split()
            dict = {'name':None,'price':None,'count':None}
            dict['name'] = l[0]
            dict['price'] = l[1]
            dict['count'] = l[2]
            res.append(dict)
            print(res)
    
    with open('fruit.txt') as f:
        res = (line.split() for line in f )
        money_l = ({'name':i[0],'price':i[1],'count':i[2]} for i in res if float(i[1])>1000)
        print(next(money_l))


##  8、函数式编程

面向过程：

优点：
1、流水线式，需要把整个流程设计出来

2、结构清晰
           
3、简化程序编程的复杂度
           
 缺点：1、扩展性差，用于不需要经常变化的软件
          
    # 仿grep -r 'python' /Users/mingleung/PycharmProjects/PythonStudyLesson/day5
    import os,time
    
    def runner(func):
        def wrapper(*args,**kwargs):
            res = func(*args)
            next(res)
            return res#得到已经next一次的res    return wrapper
    
    
    @runner
    def search(target):
        '找到文件的绝对路径’    
          while True:
            dir_name = yield        
            print('start search')
            time.sleep(3)
            g = os.walk(dir_name)
            for i in g:
                #print(i[-1])  # i[-1]是文件名            
                for j in i[-1]:
                    file_path = '%s/%s' % (i[0], j)  # 拼接                target.send(file_path)#结果传给生成器target
    @runner
    def open_file(target):
        '打开文件得到文件句柄’    
           while True:
            file_path = yield        
            print('start open')
            time.sleep(3)
            with open(file_path,encoding="ISO-8859-1") as f:
            #从windows复制过来的文件需要encoding                        
                target.send((file_path,f))
    
    @runner
    def read_file(target):
        #'获取文件内容’    
        while True:
            file_path, f= yield       
            print('start get')
            time.sleep(3)
            for line in f:
                target.send((file_path,line))
    
    @runner
    def grep(pattern, target):
        '过滤一个内容是否包含字符串python’   
           while True:
                file_path, line = yield        
                print('start grep')
                if pattern in line :
                    target.send(file_path)
    
    @runner
    def print_grep():
        '打印文件路径'   
        while True:
            file_path = yield        
            print('start print')
            time.sleep(3)
            print(file_path)
    
    
    g = search(open_file(read_file(grep('python',print_grep()))))
    g.send('/Users/mingleung/PycharmProjects/PythonStudyLesson/day5')

函数式：

编程语言定义的函数+数学意义的函数

不用变量保存、不修改变量（函数即变量）

高阶函数： 

返回值中包含函数（函数即变量）

优化：尾递归


(1)map(函数，值)

把每个值交给函数处理

    num_l = [1,2,3,1111,333]
    def map_test(func, array):
        ret=[]
        for i in array:
            res = func(i)
            ret.append(res)
        return ret
    
    print(map_test(lambda x:x+1,num_l))
    print(map(lambda x:x+1,num_l))#返回可迭代数据类型,只能迭代一次
    #for i in res:
        #print (i)
    
    print(list(res))

(2)filter(func, array)

    res=filter(func, array)#前面函数得出的布尔值，如果是True保留，否则丢弃
    list(res)
    
    name_l = [
        {’name’:’a’,’age’:10}
    {’name’:’b’,’age’:2}
    {’name’:’c’,’age’:3}
    ]
    
    filter(lambda d:d[‘age’] >3, name_l)

(3)reduce(func, array)

    对列表数据进行操作，最后得出一个数值
    num_l=[1,2,3]
    
    def reduce_test(func,array,init=None):
        if init == None:
            res = array.pop(0)
        else:
            res = init
        for num in array:
            res=func(res, num)
        return res
    
    print(reduce_test(lambda x,y:x*y,num_l))
    reduce(lambda x,y:x*y,num_l,初始值)


## 9、内置函数

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
      
    函数调用自己叫递归调用  通过栈把各个res的结果保存起来，占用内存，效率低下
    
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
        if len(list) > 1:
            mid = int(len(list)/2)
            if list[mid] == num:
                return '6666'
            elif num > list[mid]:
                list = list[mid:]
                print(list)
                return search(num,list)
            elif num < list[mid]:
                list = list[0:mid]
                print(list)
                return  search(num,list)
        else:
            if list[0] == num:
                return '666'
            else:
                return '777'
    
    print(search(101,data))






面向对象：
优点：1、扩展性强。
缺点：1、可控性差。
应用场景：互联网程序，企业内部软件，游戏

# 二、类和对象：

    class soldier:
        #提取共同的特征，组成的
        camp='china'
        def __init__(self, username):
            self.username = username
    
        def skill(self, enemy):
            print('attack to %s' % enemy)
    
    #打印返回是一个class
    #如何使用类
    # 一、类的实例化
    # 1、x=int(10)
    # 2、int.XX调用自身的方法
    #obj = Gailun() #抽象变成实际对象，实例化
    
    #二、引用类的特征（类的变量）和技能（类的函数）
    #Gailun.skill(11)
    
    #三、如何使用实例
    g = Gailun('J')#Garen.__init__(g, 'J')
    g.skill('A.enemy') #绑定方法
    print(Gailun.skill) #类的函数
    
    #总结：
    #类：一：实例化，二：引用名字（类名.变量名,类.函数名）
    #实例：引用名字（实例名.类的变量名,实例名.绑定方法，实例名.实例自己的变量名）
    
    Gailun.camp = 'lalala'
    print(Gailun.camp)
    
    g.username = 'K'
    print(g.username)
    
    del g.username
    print(g.username)
    
    g.sex = 'male'
    print(g.sex)
