# 一、面向对象
优点：扩展性强。

缺点：可控性差。

应用场景：互联网程序，企业内部软件，游戏

1、面向对象的程序设计OODesign

找对象------>归纳对象相同的特征与函数（归类）

2、面向对象编程OOPrograming 

先定义类------->实例化对象

3、OOT object oriented test测试

4、OOSM object oriendted soft maintenance维护


#定义学生类OOD

特征：共同国际'China'

技能：查看成绩，上交作业

独有的特征：名字、id 号、性别......

OOP

    class Student:
         country = 'China'
         def __init__(self, id, name, sex, province):
              self.id  = id
              self.name = name
              self.sex = sex
              self.province = province
         def search_score(self):
                   print('score')

# 二、类和对象：


    #定义学生类OOD
    # 特征(变量)：共同国际'China'
    # 技能(函数)：查看成绩，上交作业
    #
    # 独有的特征：名字、id 号、性别......
    #
    # OOP
    class Student:
        country = 'China'
        def __init__(self, id, name, sex, province):
            self.id  = id
            self.name = name
            self.sex = sex
            self.province = province
        def search_score(self):
            print('score')
        def study(self):
            print('study')
            

    #总结：
    #类：
    #一：实例化
    s1 = Student('1','A_student','mail','GD')# Student.__init__('s1','1','A_student','mail','GD')
    # 二：引用名字（类名.变量名,类.函数名）
    Student.country
    Student.search_score(s1)
    Student.x = 1#增加属性 类的名称空间
    #del Student.study#删除方法
    Student.country = 'USA' #改
    
    #实例：引用名字（实例名.类的变量名,实例名.绑定方法，实例名.实例自己的变量名）
    s1.name
    s1.study()
    s1.hobby = 'play'#增加 对象的名称空间
    #del s1.name#删除
    
    # print(Student.__dict__)#查看名称空间
    # print(s1.__dict__)
    
    print(id(s1.country)) #类的变量跟对象变量指向同一个id
    print(id(Student.country))
    
    print(id(s1.study)) #对象绑定类的方法
    print(id(Student.study)) #类调自己的函数
    

## （1）新式类：集成object的类

Python 3 类型就是类，所有类都是新式类（默认）

class A:pass

Python 2 新式类：

    class B(object):pass
    class C(B):pass

#print(B.__bases__) #打印B继承的类
#print(C.__bases__)

新式类广度优先：

    class A(object):
        def test(self):
            print('A')
    
    class B(A):
        # def test(self):
        #    print('B')
        pass
    
    class C(A):
        def test(self):
            print('C')
    
    class D(B):
        # def test(self):
        #    print('D')
        pass
    
    class E(C):
        def test(self):
            print('E')
    
    class F(D,E):
        # def test(self):
        #    print('F')
        pass
    
    f1 = F()
    f1.test()#先找f1下找test()，f1-> F-> D->B ->E->C ->A ->object
    print(F.__mro__)

    #Python 2 经典类(深度优先)、新式类跟py3一样
    
    #f1 ->F ->D ->B ->A ->E ->C



## （2）、类的交互

    #对象之间的交互
    #特征(变量)：默认皮肤，攻击力，防御力，血量，阵营
    #技能(函数)：攻击
    #独有的特征：用户名字，皮肤
    class Garen:
        camp = 'Noxus'
        def __init__(self, username, pifu='normal', gongjili = 10, xueliang = 300, fangyu = 3):
            self.usernam = username
            self.pifu = pifu
            self.gongjili = gongjili
            self.xueliang = xueliang
            self.fangyu = fangyu
        def attack(self, enemy):
            enemy.xueliang -= self.gongjili
    
    class Riven:
        camp = 'Noxus'
        def __init__(self, username, pifu='normal', gongjili = 10, xueliang = 300, fangyu = 3):
            self.usernam = username
            self.pifu = pifu
            self.gongjili = gongjili
            self.xueliang = xueliang
            self.fangyu = fangyu
        def attack(self, enemy):
            enemy.xueliang -= self.gongjili
    
    g1 = Garen('gailun')
    r1 = Riven('ruiwen')
    
    g1.attack(r1)
    print(r1.xueliang)

# 四、继承

    #继承
    #解决重用性
    class ParentClass1:
        pass
    class ParentClass2:
        pass
    class SubClass1(ParentClass1):
        pass
    class SubClass1(ParentClass1,ParentClass2):
        pass
    
    print(SubClass1.__bases__)#查看继承

例子：

    #人和猪都属于动物
    class Aniaml:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
        def walk(self):
            print('%s is walking ' % self.name)
    
        def say(self):
            print('%s is saying ' % self.name)
    
    class People(Aniaml):
        pass
    
    class Pig(Aniaml):
        pass
    
    p1 = People('A_people',19)
    p1.walk()


    #英雄联盟：盖伦和瑞文都属于英雄
    class Hero:
        def __init__(self, username, pifu, gongjili, xueliang, fangyu):
            self.usernam = username
            self.pifu = pifu
            self.gongjili = gongjili
            self.xueliang = xueliang
            self.fangyu = fangyu
        def attack(self, enemy):
            enemy.xueliang -= self.gongjili
            print('Hero attack')
        def Q_skill(self):
            print('Q')
    
    class Garen(Hero):
        camp = 'Demaxia'
        def __init__(self,username, pifu, gongjili, xueliang, fangyu,yuyin):
            Hero.__init__(self,username, pifu, gongjili, xueliang, fangyu)
            self.yuyin = yuyin
        def Q_skill(self):
            #派生
            print('demaxiya')
        def attack(self, enemy): #self = g1 ,enemy = g2
            #self.attack(enemy) #g1.attack() ,递归报错
            Hero.attack(self,enemy)#self是g1 ,调用Hero的attack方法
            print('attack from Garen')
    
    g1 = Garen('a','normal',100,3000,200,'demaxiyalalala')
    g2 = Garen('b','normal',100,3000,200,'demaxiyalalala222')
    
    g1.attack(g2)
    print(g1.xueliang)


# 五、组合

    class Teacher:
        def __init__(self, name, sex, course, birth):
            self.name = name
            self.sex = sex
            self.course = course
            self.birth = birth
    class Birth:
        def __init__(self, year, month, day):
            self.year = year
            self.month =month
            self.day = day
    
    class Course:
        def __init__(self, name, price, peroid):
            self.name = name
            self.price = price
            self.period = peroid
    
    class Student:
        def __init__(self, ID, name, course):
            self.ID = ID
            self.name = name
            self.course = course
    #组合，多个类组合到一起
    #老师有课程
    t1 = Teacher('a_teacher','male',Course('math','10000','5m'), Birth('2017','01','01'))
    
    s1 = Student(1, 'a_student', Course('python', '10000', '5m'))
    
    print(s1.course.name)
    print(t1.birth.year)


# 六、接口与归一化

    #接口与归一化
    #抽象类：本质还是类，加了装饰器，强制子类必须实现函数
    import abc
    class Animal(metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def run(self):
            raise AttributeError('must be implmented')
        @abc.abstractmethod
        def sleep(self):
            pass
        @abc.abstractmethod
        def speak(self):
            pass
    
    class People(Animal):
        pass
        # def run(self):
        #    print('People is running')
        # def sleep(self):
        #    print('People is sleeping')
    
    class pig(Animal):
        def run(self):
            print('pig is running')
        def sleep(self):
            print('pig is sleeping')
    
    p1 = People()
    p1.run()


# 七、super的用法

    #在py2只能用在新式类
    class Hero:
        def __init__(self, username, pifu, gongjili, xueliang, fangyu):
            self.username = username
            self.pifu = pifu
            self.gongjili = gongjili
            self.xueliang = xueliang
            self.fangyu = fangyu
        def attack(self, enemy):
            enemy.xueliang -= self.gongjili
            print('Hero attack')
        def Q_skill(self):
            print('Q')
        def walk(self):
            print('6666 %s'  % self.username)
    
    class Garen(Hero):
        camp = 'Demaxia'
        def __init__(self,username, pifu, gongjili, xueliang, fangyu,yuyin):
            super().__init__(username, pifu, gongjili, xueliang, fangyu)
            #在mro列表一个一个找
            #在py2里面，super(Garen, self).__init__(username, pifu, gongjili, xueliang, fangyu)
            self.yuyin = yuyin
        def Q_skill(self):
            #派生
            print('demaxiya')
        def attack(self, enemy): #self = g1 ,enemy = g2
            #self.attack(enemy) #g1.attack() ,递归报错
            Hero.attack(self,enemy)#self是g1 ,调用Hero的attack方法
            print('attack from Garen')
        def walk(self,x):
            super().walk() #此时调用的是夫类的walk()方法
            #print('子类X',x)
    
    g1 = Garen('a','normal','100','3000','80','lalala')
    g1.walk('xxx')

# 八、多态与多态性

    #多态与多态性
    
    #多态：同一种事物的不同形态，人和猪属于动物
    
    import abc
    
    class Animal(metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def run(self):
            pass
            #raise AttributeError('must be implmented')
        @abc.abstractmethod
        def sleep(self):
            pass
        def speak(self):
            pass
    
    class People(Animal):
        def run(self):
            print('People is running')
        def sleep(self):
            print('People is sleeping')
    
    class Pig(Animal):
        def run(self):
            print('pig is running')
        def sleep(self):
            print('pig is sleeping')
    
    p1 = People()
    p1.run()
    pig1 = Pig()
    pig1.run()

    def func(obj):#传入不同的值
        obj.run() #调用逻辑都一样
    #多态性依赖于继承  
    #多态性：定义统一个接口实现不同的执行效果
    func(p1)
    func(pig1)

# 九、封装

    #第一层面：定义一个类
    
    #第二层面：
    class A:
        __x = 1#隐藏
        def test(self):
            print('A')
        def tell(self):
            print(self.__x)
        def __fa(self):
            print('A')
        def tell_fa(self):
            self.__fa()
    
    # print(A.__dict__)
    # print(A._A__x)
    
    #__名字，这种语法只在定义的时候才有变形的效果，如果类或对象已经产生了，就不会有变形效果
    #__名字的函数，不能被子类继承

# 十、property

    #把方法变成属性
    #1、调用形式统一 2、封装
    
    import math
    class Circle:
        def __init__(self, r):
            self.r = r
        #优先于对象的属性
        @property #area = property(area)
        def area(self):
            return math.pi * self.r**2
    
        @property
        def perimeter(self):
            return 2 * math.pi * self.r
    
    c = Circle(7)
    # print(c.area())
    print(c.area)
    
    class People:
        def __init__(self, name):
            #self.__name = name
            self.name = name
    
        @property#查询用
        def name(self):
            return self.__name
    
        @name.setter#赋值
        def name(self, value):
            if not isinstance(value, str): #设定传入值必须是str，否则报错
                raise TypeError('must be str!')
            self.__name = value
    
        @name.deleter#删除
        def name(self):
            del self.__name
    
    # a = People('a')
    # print(a.name)
    #del a.name
    #print(a.name)

# 十一、classmethod

把一个方法绑定给类，”类.方法()”，会把类本身当做第一个参数自动传给方法

    #classmethod
    class Foo:
        def bar(self):
            print('baraaaaaa')

    @classmethod  #把一个方法绑定给类，" 类.方法（）"，会把类本身当做第一个参数自动传给方法
    def test(cls, x):  #拿到类的内存地址，可以实例化或引用类的属性
        a = cls()
        a.bar()
        print(cls, x)
        
    f = Foo()
    print(f.bar)
    
    Foo.test(1)

## (1)、__str__用法
    #定义在类内部，必须返回字符串类型
    #打印由这个类产生的对象 ，会触发__str__
    class People:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    def __str__(self):#打印p1 ，会触发此类
        #定义在类内部，必须返回字符串类型
        return 'name:%s age:%s' % (self.name,self.age)

    p1 = People('A',17)
    print(p1)


（2）、classmethod用法
    import time
    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day
    
        @classmethod
        def now(cls):
            print(cls)
            t = time.localtime()
            return cls(t.tm_year, t.tm_mon, t.tm_mday)
    
    
    class EuroDate(Date):
    
        def __str__(self):
            return 'year:%s. month:%s day:%s'%(self.year,self.month,self.day)
    
    e1 = EuroDate.now()
    print(e1)


十二、staticmethod

    class Foo:
        @staticmethod #self也要传值，self不是绑定方法，不能自动传值
        def spam(self,y,z):
            print('--->',self,y,z)
    
    #Foo.spam(1,2,3)
    f1 = Foo()
    f1.spam(1,2,3)

    例子：
    import time
    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day
    
    
        @staticmethod
        def now():
            t = time.localtime()
            return Date(t.tm_year, t.tm_mon, t.tm_mday)
    
        @staticmethod#给类用的方法，没有自动传值功能#原绑定方法有自动传值功能
        def tomorrow():
            t = time.localtime(time.time() + 86400) #time.time()时间戳1970年开始
            return Date(t.tm_year, t.tm_mon, t.tm_mday)
    
    #都用相同实例化方式
    d1 = Date(2017,1,1)
    d2 = Date(2017,1,1)
    d_now = Date.now()
    print(d_now.year, d_now.month, d_now.day)
    d_tor = Date.tomorrow()
    print(d_tor.year, d_tor.month, d_tor.day)


十三、反射

    #通过字符串形式调用
    class People:
        country = 'China'
        def __init__(self, name):
            self.name = name
        def walk(self):
            print('walking')
    p = People('A')
    
    #hasattr
    print(hasattr(p, 'country')) #对象，是否有属性
    print(hasattr(People, 'country'))#类，是否有属性
    
    #getattr 拿到属性的值(常用)
    res = getattr(People, 'country')
    print(res)
    
    f = getattr(p, 'walk')
    print(f)
    f() #对象的绑定方法自动传值
    
    f1 = getattr(People, 'walk')
    print(f1)#函数不能自动传值
    f1(p)
    
    print(getattr(p, 'XXXXX', '没有此属性')) #保证不会抛出异常
    if hasattr(p, 'walk'):
        func = getattr(p, 'walk')
        func()
    
    #setattr 设置属性的值(常用)
    setattr(People, 'country', 'USA')
    print(getattr(People, 'country'))
    
    #delattr 删除属性的值
    #delattr(People, 'country')
    #print(getattr(People, 'country'))
    
    #定制数据类型
    #isinstance(obj, cls) 检查是否obj是否是cls的类的对象
    #issubclass(sub, super) 检查sub类是否是super 类的派生类
    
### 1、反射当前模块的属性通过字符串形式操作对象相关的属性

    #例子一：
    import sys
    
    x = 111111111111
    class Foo:
        pass
    
    def s1():
        print('s1')
    
    def s2():
        print('s2')
    
    this_module = sys.modules[__name__]#拿到当前模块的对象
    print(this_module)
    print(__name__)



    例子二：
    import sys
    
    def add():
        print('add')
    
    def change():
        print('change')
    
    def delete():
        print('delete')
    
    this_modules = sys.modules[__name__]
    
    # func_dict = {
    #    'add':add,
    #    'change':change,
    #    'delete':delete,
    # }
    while True:
        cmd = input('Please input cmd: ').strip()
        if not cmd :continue
        if hasattr(this_modules, cmd):
            f = getattr(this_modules, cmd)
            f()


# 十四、可插拔

    import kechaba_client
    
    f1 = kechaba_client.Ftp_Client('192.168.0.1')
    
    #如果有get()就执行，如果没有就执行其他逻辑(反射)
    if hasattr(f1, 'get'):
        func = getattr(f1, 'get')
        func()
    
    #可插拔
    
    class Ftp_Client:
        def __init__(self, addr):
            print('正在连接服务器%s' % addr)
            self.addr = addr
    
        def get(self):
            print('get successful')
    
        def put(self):
            pass


# 十五、二次加工数据类型

    #基于继承的原理二次加工
    class List(list):
    
        def append(self, p_object):
            print('------>', p_object)
            if not isinstance(p_object, int):
                raise TypeError('must be str')
            super().append(p_object)
    
        def insert(self, index: int, p_object):
            if not isinstance(p_object, int):
                raise TypeError('must be str')
            super().insert(index, p_object)
    
        @property
        def mid(self):
            index = len(self) // 2
            return self[index]
    
    l1 = List([1,2,3])
    print(l1)
    l1.append(2)
    print(l1)
    
    l1.insert(0, 3333)
    print(l1)
    
    f = open('a.txt','w')
    print(f)

    import time
    #类不能继承函数
    #基于授权来定制自己的数据类型
    class Open:
        def __init__(self, filepath, mode='r', encoding='utf-8'):
            self.f = open(filepath, mode=mode, encoding=encoding)
            self.filepath = filepath
            self.mode = mode
            self.encoding = encoding
    
        def write(self, line):
            #调用真实的write
            t = time.strftime('%Y-%m-%d %X')
            self.f.write('%s %s' % (line, t))
    
        def read(self):
            print('read')
    
        def __getattr__(self, item):
            #print('____',item)
            return getattr(self.f, item)
    
    f1 = Open('b.txt', 'w')
    # print(f1)
    f1.write(11111)
    
    f = Open('b.txt', 'r')
    print(f.read())


# 十六、通过字符串导入模块

    #推荐
    import importlib
    
    t = importlib.import_module('time')
    print(t.time())
    


# 十七、上下文管理协议

    # with open('a.txt') as f:
    #    print('lalala')
    #    print(f.read())
    
    class Foo:
        def __init__(self, filepath, mode='r', encoding='utf-8'):
            self.f = open(filepath, mode=mode, encoding=encoding)
    
        def write(self, line):
            self.f.write(line)
    
        def __getattr__(self, item):
            return getattr(self.f, item)
    
        def __enter__(self):
            return self #拿到真实的文件句柄
    
        #触发异常就执行exit里面的代码
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.f.close()
            print('exite')
            print('exc_type', exc_type)
            print('exc_val', exc_val)
            print('exc_tb', exc_tb)
    
    with Foo('a.txt') as f1: # f1 = Foo().__enter__()
        print(f1.read())
        #raise NameError('Name_erroe')
        

    #__del__析构函数，清理操作
    class Open:
        def __init__(self, filepath, mode='r', encoding='utf-8'):
            self.f = open(filepath, mode=mode, encoding=encoding)
    
        def write(self, line):
            self.f.write(line)
    
        def __getattr__(self, item):
            return getattr(self.f, item)
    
        def __del__(self):
            #写入清理操作
            print('---a')
            self.f.close()
    
    f = Open('a.txt','w')
    del f #删除对象执行__del__析构函数，或者引用计数结束

# 十八、attr系列

    #__setattr__, __getattr__, __delattr__
    
    class Foo:
        def __init__(self, name):
            self.name = name
    
        #给对象设置属性，就会触发setattr
        def __setattr__(self, key, value):
            if not isinstance(value, str):
                raise TypeError('must be str')
            print('setattr----key: %s, %s' % (key, value))
            print(type(key))
            #不能使用setattr()设置，会造成递归报错
            self.__dict__[key] = value
    
        def __delattr__(self, item):
            print('delattr: %s' % item)
            self.__dict__.pop(item)
    
        def __getattr__(self, item):
            #属性不存在就会触发
            print('getattr: %s %s' % (item, type(item)))
    
    f1 = Foo('a')
    # f1.age = '18'
    # del f1.age
    # print(f1.age)
    print(f1.xxxxxxx)

# 十九、item系列
    #以字典形式，操作属性
    class Foo:
        def __init__(self,name):
            self.name = name
    
        def __getitem__(self, item):
            return self.__dict__[item]
    
        def __setitem__(self, key, value):
            print('set successful')
            self.key = value
    
        def __delitem__(self, key):
            print('delete')
            self.__dict__.pop(key)
    
    f = Foo('aaa')
    
    f['age'] = 18
    
    print(f.__dict__)
    
    #中括号才能触发__getitem__
    print(f['name'])

# 二十、__slots__

    class Foo:
        #1、对象不能产生名称空间__dict__
        #2、属性只能设置__slots__有的属性
        #3、节省内存，用于一个类要产生多个对象，而属性相同
        __slots__ = ['x']
    
    f = Foo()
    print(f.__slots__)
    f.x = 1
    print(f.x)
    
    from collections import Iterator, Iterable
    class Foo1:
        def __init__(self, start):
            self.start = start
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self.start == 10:
                raise StopIteration
            n = self.start
            self.start += 1
            return n
    
    # f1 = Foo1(0)
    # print(isinstance(f1, Iterator))
    # obj = f1.__iter__()
    # print(obj.__next__())
    # print(obj.__next__())
    # print(obj.__next__())
    
    # for i in obj:
    #    print(i)

    #模拟range
    
    class Range:
        'lalalala'
        def __init__(self, start, stop):
            self.start =  start
            self.stop = stop
    
        def __iter__(self):
            return self
    
        def __next__(self):
            if self.start == self.stop:
                raise StopIteration
            n = self.start
            self.start +=1
            return n
    
    r = Range(0,10)
    print(r.__doc__)
    for i in r:
        print(i)
    
    print(r.__module__)



# 二十一、元类、__call__

    class People:
        def __init__(self, name):
            self.name = name
        #变成可调用对象
        def __call__(self, *args, **kwargs):
            print('call')
    
    # p = People('a')
    # p()#找自己的__call__绑定方法
    # print(callable(p))
    # print(callable(People))
    # #由type产生的
    # print(type(People))
    
    

---


    #模拟创建类
    #type成为元类，实例化一个类，不用class关键字
    #元类是类的类，控制类的行为
    
    def run(self):
        print('%s  run' % self)
    class_name = 'bar'
    class_dic={
        'x':1,
        'run':run,
    }
    # bases = (object,)
    #
    # bar = type(class_name,bases,class_dic) #创建类的另一种发发
    # print(bar)
    
    #定制自己的类
    class Mymeta(type):
        def __init__(self, class_name, class_bases, class_dic):
            print(class_name)
            print(class_bases)
            print(class_dic)
            print(self)
            # 定制必须写__doc__
            #判断class_dic 是否可调用，
            # '__init__': <function Foo3.__init__ at 0x00616DF8>可以调用的话
            #找.__doc__，再判断是否为真，
            for key in class_dic:
            
                if not callable(class_dic[key]): continue
                if not class_dic[key].__doc__:
                    raise TypeError('must writing __doc__')
    
        # type.__init__(self,class_name, class_bases, class_dic)
    
        def __call__(self, *args, **kwargs):
            print(self)#self就是 <class '__main__.Foo3'>
            obj = self.__new__(self) #产生空对象
            self.__init__(obj, *args, **kwargs)#初始化 obj.name = 'bbb'
            return obj
    
    #默认type: type('Foo', (object,), {'x':1,'run':run })
    #现在Mymetea: Mymetea('Foo', (object,), {'x':1,'run':run })
    class Foo3(metaclass=Mymeta):
        'foo3'
        x = 1
        def __init__(self, name):
            'init'
            self.name = name
        def run(self):
            'run'
            print('running')
    
    f1 = Foo3('bbb')#Foo3是Mymeta的对象，Foo3()就是调用类的__call__方法,产生空对象
    print(f1)


# 二十二、time模块

    import time
    
    print(time.time())#打印时间戳，从1970年到现在的秒数
    
    t = time.localtime('可以传入秒进行转换，默认是今天')#结构化时间，对时间进行操作，time.struct_time(tm_year=2017, tm_mon=6, tm_mday=23, tm_hour=15, tm_min=15, tm_sec=45, tm_wday=4, tm_yday=174, tm_isdst=0)
    
    
    print(t)
    print(time.strftime('%Y-%m-%d %X %z'))#字符串时间 2017-06-23 15:16:14 +0800
    
    print(time.gmtime()) #世界标准时间的结构化时间 ， time.struct_time(tm_year=2017, tm_mon=6, tm_mday=23, tm_hour=7, tm_min=16, tm_sec=51, tm_wday=4, tm_yday=174, tm_isdst=0)
    
    print(time.mktime(t))#传入结构化时间------>返回时间戳 
    
    print(time.ctime(‘传入秒数,默认今天’))#时间戳----->字符串  
    
    print(time.asctime(time.localtime(234523453)))#结构化时间
    
    
    结构化时间 --- > 时间戳 ： mktime()
    时间戳 ---- > 字符串 ： ctime()
    时间戳 ---- > 结构化时间 : localtime()

    #设a为字符串
    import time
    a = "2011-09-28 10:00:00"
    
    #中间过程，一般都需要将字符串转化为结构化时间
    time.strptime(a,'%Y-%m-%d %H:%M:%S')
    >>time.struct_time(tm_year=2011, tm_mon=9, tm_mday=27, tm_hour=10, tm_min=50, tm_sec=0, tm_wday=1, tm_yday=270, tm_isdst=-1)
    
    #将"2011-09-28 10:00:00"转化为时间戳
    time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
    >>1317091800.0
    
    #将时间戳转化为localtime
    x = time.localtime(1317091800.0)
    time.strftime('%Y-%m-%d %H:%M:%S',x)
    >>2011-09-27 10:50:00


# 二十三、random 模块

    import random
    print(random.random()) #0 - 1 浮点数字
    print(random.randint(1,5)) #1 - 5 整形数字
    print(random.randrange(1,5)) #顾头不顾尾
    print(random.choice([1,2,3,4,55555])) #在列表里随机选择
    print(random.sample([1,2,3,4,55555],2)) #在列表里随机选择 2 个
    
    print(random.uniform(1,3)) #大于1小于3的浮点型数
    
    item = [1,3,6345,312]
    random.shuffle(item) #重新排序
    print(item)
    
    #随机数字加字母
    def validate():
    
        s = ''
        for i in range(5):
            r_num = random.randint(65,90)
            r_alph = chr(r_num)
            r_alph = random.choice([r_num, r_alph])
            s += str(r_alph)
        return s
    
    print(validate())



# 二十四、hashlib

    import hashlib
    
    md5 = hashlib.md5('matt'.encode('utf8')) #加源，让md5加密复杂化
    
    md5.update('hello'.encode('utf-8')) #5d41402abc4b2a76b9719d911017c592
    md5.update('hello'.encode('utf-8')) #已经是hellohello的结果:23b431acfeb41e15d466d75de822307c
    
    print(md5.hexdigest())

# 二十五、os

    #与操作系统交互的一个接口
    import os
    
    print(os.getcwd())# 拿到当前路径
    
    f = open('test.txt','w')
    
    os.chdir('G:\\untitled\\')#修改路径
    
    os.curdir() #返回当前目录
    
    os.pardir() #返回父级目录
    
    os.makedirs('aaa')
    
    os.chdir('aaa')
    
    print(os.getcwd())
    
    os.removedirs('aaa') #若目录为空删除，并递归到上一级，若为空则删除
    
    os.rmdir('aaa') #删除单层目录
    
    print(os.listdir()) #目录下所有文件及文件夹，放入列表
    
    print(os.stat(r'G:\\untitled'))
    '''
    os.stat_result(st_mode=16895, st_ino=6192449487655633, st_dev=94124, st_nlink=1,
    st_uid=0, st_gid=0, st_size=4096, st_atime=1497924646, st_mtime=1497924646,
    st_ctime=1496219244)
    '''
    os_t = os.stat(r'G:\\untitled').st_ctime
    print(time.localtime(os_t))
    
    #os.sep # win ："\\"  Linux ： "/"
    'day' + os.sep + '777' #处理路径
    #os.pathsep 输出用于分割文件路径的字符串，win: 分号 ； Linux 冒号：
    
    # print(os.name) #nt ：windows 操作系统
    # print(os.system('dir'))# 交互式命令
    
    dir = os.path.abspath('test.txt') #返回绝对路径
    
    print(os.path.basename(dir)) #test.txt
    print(os.path.dirname(dir)) #G:\untitled\day7
    
    print(os.path.exists('test.txt'))# 判断是否存在
    
    #-------------------重点-----------------
    #路径拼接
    s1 = r'D:\untitled'
    s2 = r'day8'
    res = os.path.join(s1, s2)
    print(res)
    
    os.path.getatime('test.txt') #返回文件或文件夹最后存取时间
    os.path.getmtime('test.txt') #返回文件或者目录最后修改时间


# 二十六、sys

    import sys
    
    # print(sys.version) #打印解释器版本 少用
    # print(sys.platform) #win32 打印操作系统系统 = os.name 少用
    
    #在运行程序前可输入信息
    print(sys.argv)
    
    username  = sys.argv[1]
    passwd  = sys.argv[2]


# 二十七、logging

    import logging
    
    #设置格式
    
    #配置的两种方式： 1、config 2、logger(常用)
    
    #1、config
    # logging.basicConfig(level=logging.DEBUG,
    #                    format='%(asctime)s----%(message)s----%(lineno)d',
    #                    datefmt='%Y-%m-%d %X %z',
    #                    filename='log',
    #                    filemode='a'
    # )
    #%(lineno)d 日志所在的代码行
    
    def logger():
        #2、logger(常用)
        logger = logging.getLogger()
    
        #文件流
        fh = logging.FileHandler('log2')
    
        #屏幕流
        sh = logging.StreamHandler()
    
        #设置等级
        logger.setLevel(logging.DEBUG)
    
        #格式对象
        fm = logging.Formatter(fmt='%(asctime)s----%(message)s----%(lineno)d',
                              datefmt='%Y-%m-%d %X %z')
    
        #设置
        fh.setFormatter(fm)
        sh.setFormatter(fm)
    
        #添加handler
        logger.addHandler(sh)
        logger.addHandler(fh)
    
        #logging 五个等级
        logging.debug('debug')
        logging.info('info')
        logging.warning('warning')
        logging.error('error')
        logging.critical('critical')
    
        return  logger
    
    logger()


# 二十八、json

    import json
    
    d = {
        'China':['GD','BJ'],
        'Canada':['AN']
    }
    
    j_d = json.dumps(d) #把d转换成json字符串
    with open('json.txt','r') as f:
        file = f.read()
        #拿到的是json字符串，需要反序列才能成为字典    data = json.loads(file)
        print(type(data)) #此时才是字典格式
    #dump#省略了write那一步f = open('json.txt','w')
    json.dump(d, f)
    
    
    #------------------i = 10s = 'hello't = (1, 5, 7)
    l = ['qw', 1, 'ewq']
    d = {'a':1, 'b':'2'}
    
    json_i = json.dumps(l)
    #打印的数据类型是json的数据类型，用于方便不同程序之间交流#print(json_i)
    with open('test.txt', 'r') as f:
        data = f.read()
        data_d =  json.dumps(data)
        dict_j = json.loads(data_d)
        print(dict_j)
    #满足json格式的文本就能loads,反序列化回去原来格式

# 二十九、pickle
    用法跟json 一样
    import datetime
    import json
    import pickle
    t = datetime.datetime.now()
    
    d = {"date":t}
    
    # json.dump(d, open("jason_1.txt", 'w'))
    #pickle处理成字节数据
    pickle_d = pickle.dumps(d)
    print(pickle_d)
    
    # f = open('pickle_1.txt', 'wb')#写入字节数据要加b
    # f.write(pickle_d)
    
    # f = open('pickle_1.txt', 'rb')
    # data = pickle.loads(f.read())
    # print(data)
    
    # f = open('pickle_2.txt', 'wb')
    # f.write(pickle_d)
    f = open('pickle_2.txt', 'rb')
    data = pickle.loads(f.read())
    print(data)

# 三十、正则

    import re
    #正则表达式：对字符串模糊匹配
    
    #原则符
    #'\d'分别取出数字
    #'\d+'取出数字并连接
    d = re.findall('\d+','wqejda23432sduash121321da')
    print(d)
    
    # . 可以代表除换行符号以外的任意一个字符
    d = re.findall('p..h','hello python')
    print(d) #['pyth']
    
    # * 可以代表[0,∞]个字符
    d = re.findall('ab*c','abbbc')
    print(d) #['abbbc']
    
    # + 可以代表[1,∞]个字符
    d = re.findall('b+c','bbbbc')
    print(d) #['bbbbc']
    
    # ？可以代表[0,1]个字符
    d = re.findall('b?c','bbbbc')
    print(d) #['bc']
    
    #{} 可以代表{N, M}个字符
    d = re.findall('020\d{8}','bcsabbbc02088888888')
    print(d) #['02088888888']
    #{0,}代表∞
    
    #字符集[] ,取其中一个
    d = re.findall('a[abc]c','abc,aac,acc,aec')
    print(d) #['abc', 'aac', 'acc']
    
    d = re.findall('a[b*]c','a*c,aac,acc,aec')
    print(d) #['a*c']
    
    # [^ - ]
    d = re.findall('[a-zA-Z0-9]+','dasASDwad2013214daw')
    print(d) #['dasASDwad2013214daw']
    
    #取反
    d = re.findall('[^2]*','dasASDwad2013214daw')
    print(d) #['dasASDwad', '', '013', '', '14daw', '']
    
    # ^ 从头开始匹配
    d = re.findall('^020\d{8}','02066666666feiuwf')
    print(d) #['02066666666']
    
    # $ 从结尾匹配
    d = re.findall('ming$','02066666666feiuwfming')
    print(d) #['ming']
    
    #()分组，只取分组内容
    #命名分组
    #?P<author> 起名
    ret1 = re.search(r'(?P<author>\w+)\.index\.(?P<id>\d+)','matt.index.111')
    print(ret1.group('author'))
    
    #?:取消优先级，取匹配到的全部内容
    d = re.findall('(?:\d)+iuw','02066666666765iuwfming')
    print(d) #['02066666666765iuw']
    
    # | ：或
    d = re.findall('www\.(?:baidu|google)\.com','www.google.com')
    print(d) #['www.google.com']
    
    # \ ：转义 能让原则符变成普通符号（\.），能让普通符号变成原则符(\d：匹配数字,\s：匹配字符，\w：匹配)
    d = re.findall('\d+\.?\d*\*\d+', '2.2*7+3213-5432*3')
    
    print(d)
    
    #\d 任何十进制数 [0-9]
    #\D 任何非数字字符[^0-9]
    #\s 匹配任何空白字符 [\t\n\r\f\v]
    #\S 匹配任何非空白字符[^\t\n\r\f\v]
    #\w 匹配任何字母数字字符 [a-zA-Z0-9]
    #\W 匹配任何非字母数字字符[^a-zA-Z0-9]
    #\b 匹配一个特殊字符边界，空格、&、#等
    
    #python 解释器 \ 是转义的意思 ，第一步 \\ -> \ ,re模块拿到\\ ，才能得到\的普通符号
    print(re.findall('c\\\\l','abc\l'))
    
    #re 的方法
    #re.findall()
    
    #re.finditer 返回迭代器
    d = re.finditer('\w','asdadasdads')
    for i in d:
        print(i.group())
    
    #re.search 如果能匹配,返回对象,否则为None    group()方法取得具体内容
    print(re.search("\d+","qwe223edqw"))
    #'(3+7*2+(5*6-3)+7+(10\2+1))+3'
    
    #re.split('分隔符','字符串','分割次数'默认0) 按条件分割
    print(re.split('1','ewq1ewqe1eqwrt',1)) #['ewq', 'ewqe', 'eqwrt']
    
    #re.sub('替换内容'，'替换成此内容', '字符串','替换次数')
    print(re.sub('o','222','hello world')) #hell222 w222rld
    
    #re.subn('替换内容'，'替换成此内容', '字符串','替换次数')
    print(re.subn('o','222','hello world')) #('hell222 w222rld', 2)
    
    #re.comiple 一次完成编译规则
    ret = re.compile("\d+")
    print(ret.findall('ew23ewq432'))
    
    print(ret.sub('我是数字','ewq222ewq444rwe666'))
    
    #贪婪匹配
    print(re.findall('[0-9]+','eqw231312eqw312321')) #['231312', '312321']
    
    #非贪婪匹配
    print(re.findall('[0-9]+?','eqw231312eqw312321')) #['2', '3', '1', '3', '1', '2', '3', '1', '2', '3', '2', '1']

# 三十一、异常处理
1、由语法上引发的异常（在程序执行前就改正）
2、由逻辑上引发的异常（用if提前预防，没办法预知时用try except）

    l = [1,2,3,4,5,6,7,8]
    
    index = 1000
    try:
        print(l[index])
    except IndexError as e :
        print('继续执行')
    
    print(6666) #用try except 之后就能在捕捉错误后继续运行
    
    try:
        print(x)
        l = [1,2,3]
        l[1000]
        d = {'a':1}
        d['b']
    
    #跟if多分支类似，执行了其中一个就停止了。
    except KeyError:
        pass
    except ValueError:
        pass
    except Exception:#万能捕捉异常
        print('eeee')
    else:
        print("没有异常")
    finally:
        print('无论有无异常都执行该模块，通常是清理工作')
    
    #try except : 无法预测的异常发生时，捕捉异常
    #if else : 预防异常发生
    
    #主动触发异常
    #raise IndexError('lalalala')
    
    #自定义异常
    # class DesginError(BaseException):
    #    def __init__(self, msg):
    #        self.msg = msg
    #    def __str__(self):
    #        return  self.msg
    #
    # raise DesginError('54312')
    
    #断言
    #程序运行到此处 x 一定要等于 1 才会往下走
    x = 1
    assert x == 1
    print('====>')

# 三十二、模块路径搜索


    #优先从内存中找，再找内建，最后再找sys.path中一个一个路径找
    import sys
    sys.path.append(r'G:\untitled\day6')
    import CRM
    print(sys.modules)
    print(sys.path)
    
    
    #遵循原则：用import 导入内置模块、第三方模块
    #          避免import 导入自定义模块，应该用from import 的相对路径导入（from . import XXX）
    
    # import glance.api.policy #.的左边必须是包，包是含有__init__.py文件的文件夹
    #
    # glance.api.policy.get()
    #
    # from glance.api.policy import get #import 右边只能是单独的包或者文件
    #
    # get()
    #
    # from glance.api import policy #import 右边只能是单独的包或者文件
    #
    # policy.get()
    #
    # #包的导入就会执行包下的__init__.py下的文件
    
    # from glance.api import * #包的导入就会执行包下的__init__.py下的文件, * 代表init文件里面的变量名字
    # print(policy)
    
    #绝对导入 以本文件的sys.path 为准
    #相对导入
    # import glance.api
    # print(glance.api.policy)
    #
    # glance.api.main()
    
    import glance
    
    glance.get()
    glance.main()
    glance.create_resource('111')




