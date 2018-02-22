# Python 基础

### 一、函数

定义：自足含有某些功能的代码块

作用：

1. 解决代码重用问题
2. 提高可读性
3. 统一维护

<br>

####  参数传递

&emsp;&emsp;一个可变对象（list, dict, tuple, set）传入到函数时，函数内的引用指向该可变对象同一个内存地址，就会引发该对象的改变。而不可变对象（string, int…），传递给函数时会自动复制一份，指向另一个内存地址，所以不会造成该对象的修改。

<br>

&emsp;&emsp;*args：接收未捕捉的参数，形成元组

&emsp;&emsp;**kwargs：接收未捕捉的键值对函数，形成字典

<br>

#### 名称空间

内置名称空间 ：dir(builtins)  查看

全局名称空间：py 文件中没有缩进的定义

局部名称空间：函数内部的定义

<br>

闭包：内部函数包含对外部函数变量的引用，称为闭包

<br>

#### 装饰器

定义：不改变原代码的前提下，新增额外的功能（利用作用域实现）

<br>

#### 生成器

定义：含有 yield 的函数称为生成器，其本质是含有 \_\_iter_\_ 和 \_\_next\_\_ 方法的函数，也是一个迭代器

注意：

1. next、send 方法都能让生成器函数继续运行，直到遇到下一个 yield 
2. 如果 yield 是等式，需要 next() 激活后才能调用 send() 传值
3. 如果 yield 是等式，调用 send() 方法先赋值再往下执行

<br>

### 二、面向对象设计

&emsp;&emsp;面向对象设计是一种程序设计的思想，通过定义含有所需功能的类，并调用实例化对象完成一些列的操作

&emsp;&emsp;优点：扩展性强

&emsp;&emsp;缺点：可控性差，无法预测程序执行过程

<br

> 面向过程编程：流水式的程序设计
>
> 优点：降低程序复杂度
>
> 缺点：可扩展性差，只能解决某一种特定的问题

<br>

#### 接口：

&emsp;&emsp;定义：把自己提供给外界的一种抽象物

&emsp;&emsp;python 中通过继承 abc 以及添加 abstractmethod 装饰器实现

 <br>

#### 继承：

&emsp;&emsp;新式类：广度优先（py2中需要继承 object)

&emsp;&emsp;经典类：深度优先

<br>

#### super：

&emsp;&emsp;调用父类的 \_\_init\_\_ 方法，使用规则 super(当前类名, self).\_\_init\_\_(其余参数) 

<br>

#### property:

&emsp;&emsp;把方法变成属性，隐藏具体实现逻辑

&emsp;&emsp;配合 setter. deleter 装饰器隐藏属性的操作过程

<br>

#### staticmethod:

&emsp;&emsp;静态方法，类里面的方法不需要绑定对象，供类使用

<br>

#### classmethod:

&emsp;&emsp;类方法，类里面的方法绑定当前的类，也就是当前类作为参数传入到方法中，供方法使用

<br>

#### 元类：

&emsp;&emsp;对象由类产生，类由元类产生，也就是说是类的“类”。

&emsp;&emsp;作用：控制类的产生

&emsp;&emsp;用法：type(class_name, (class_bases, ), class_dict)

<br>

#### \_\_call\_\_ 方法：

&emsp;&emsp;类 + () 执行它的  \_\_call\_\_ 方法

&emsp;&emsp;实例化一个类的对象，本质是调用元类的 \_\_call\_\_ 方法，生成空对象并调用 \_\_init\_\_ 方法

````Python
class MyMeta(type):
    def __init__(self, class_name, class_bases, class_dict):
        pass

    def __call__(self, *args, **kwargs):
        '''
        self: 当前的类      
        --------------------------------
        1. 调用 new 方法创建空对象
        2. 调用当前类的构造方法并传入空对象及参数
        3. 返回对象
        '''
        obj = self.__new__(self)
        self.__init__(obj, *args, **kwargs)
        return obj

class Foo(metaclass=MyMeta):
    x = 1
    def __init__(self, name):
        self.name = name

    def run(self):
        print('run')

foo = Foo('eee')
print(foo)
````





