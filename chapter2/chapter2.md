# 一、PYTHON 
1、编译型语言

人类看懂的代码---->翻译成机器语言（0101010）

c c++ go swift object-C Pascal

gcc hello.c 手动翻译

效率低 依赖平台 不能跨

2、解释型语言

读一行翻译一行  #shell 程序的解释器

javascript python ruby ruby

效率低 跨平台 开发效率高 不需要关注底层 学习成本的低

变量：是容器，存储数据到内存

变量的规范：字母、数字、下划线的任意组合

第一个字母不能是数字

关键字不能声明为变量

下滑线体 python 官方推荐

大写是常量   #AGE=12

3、用户输入

    name = input ("Please input “)

Control D 复制加粘贴
Control ? 全注释

4、数据类型

int 整型 

long 长整型 python3已经没有了

float 浮点型 有理数中某特定子集的数字表示

str 字符串 

Bool 布尔

Dict 字典

List 列表

Set 集合

Bytes 字节 ——是一个8bits的字节

所有字符存到内存里，都是bytes格式

Python2 看到的字符串是bytes == str.  unicode == unicode(python3 str )

强制转换会把字符变成bytes

Python3
1、所有字符在内存里都是unicode编码
2、pycharm解释器读取文件的默认编码是utf8
3、 有一个文件编码是GBK，读取时，需要encoding=‘GBK’ 
4、str == unicode. (也是一种bytes)
   bytes == bytes.  
5、存入硬盘和网络发送的文件要转换成bytes ——>encode(‘UTF-8')                                

    IndentationError :expected an intended block 缩进错误


5、ASCII 美国标准信息交换代码
GB2312   6700个字  字符编码 BIG5 繁体中文
GBK1.0.  21000个字
GB18030  27000个字
Unicode  统一编码.   Utf-8可变长编码 ：英文占1个字节，中文占3个字节
8bits = 1Byte = 1 字节 

6、注释

、# ——单行

“”“   ”“” ——多行  变成字符串不能执行，但是赋值后可以打印


7、切片

    print (name.strip()) #脱掉制表符、空格、换行#
    print(name.split()) #按空格分割成为列表#
    print(len(name)) #长度25
    print(name[0::2]) #步长为2切片


    name = “aaaabbbccc”
    
    print( name.index(‘a’)) #索引 返回0
    
    name[0:8] # 切片第一位到第八位
    
    切片原则：顾头不顾尾
    
    [0::2]# 步长两个切片
    

*pycharm技巧：按住Ctl 指向方法，进入源码看解释
                        

    print(names.count('apple'))#统计
    names.append('watermelon') #追加
    names.insert(1,'kiwi') #插入第二位上
    names.pop(4) #删除
    names.remove("apple") #默认删除第一个
    def names[1] #删除第一个
    names[names.index("watermelon")] = ‘kiwi’ #修改
    name.clear() #清空列表
    name.extend(names2) #扩展
    name.reverse() # 反转
    name.sort() #排序。py3不能不同格式数据排序


8、循环

(1)

    for i in range(10):
        ……
        break#跳出整个循环
        continue #跳出本次循环
    else:  #正常循环结束就执行for else里面的内容
        XXX


(2)

while:

else:

10、字典
    
    Key : value 
    name = {440104XXXX:{ ’name’:’Matt’, ‘age’:25},
     
    }

11、字符串格式化

    Msg = ‘’ hello %s python lalalal’’  
    Msg % (‘world’)

12、运算符

% 取余——判断奇偶数 

// 取整除 ——取小数点前一位

身份运算：

type(1) is int

位运算：转换为二进制在进行与、或、异或、取反、左移动、右移动

\&

\|

\^

\-

\<<

\>>

13、copy

（1）列表存的是内存地址，指向真正存值的内存地址
Copy 只复制内存地址，并没有真正复制值

fromkeys([1,2,3],’test’) 生成字典

14、三元运算

    a = 3 
    b = 5
    c = a if a < b else b #如果a<b ,把a赋给c ,否则把b赋给c
                          #(可以套三元运算)

15、进制
Python >> oct() #八进制转换

hex() #十六进制转换

十六进制：0123456789ABCDEF（占4个二进制位）


16、元组

用于存储数据，但它是只读

    name = (‘aaa’,’bbbb’)
    dir(name) #把传入的数据类型的所有方法，以列表形式返回
    
    list(name) #转换为列表

17、集合

关系测试

交集 两个都有

差集  列表a有，b没有

并集  两个列表里的元素合并在一起，

特点：去重，无序

    linux = [‘a’, ‘b’ , ‘c’]
    python = [ ‘a’, ‘b’ ]
    
    linux = {‘a’, ‘b’ , ‘c’} #{}是集合，没有value,无序的
    python = { ‘a’, ‘b’ }
    
    l_p =[ ]
    
    for i in python :
        for i in linux :
            l_p.append(i)
    #交集部分取出来
    
    linux.intersection(python) #交集
    linux & python #同上 
    linux.difference(python)#差集
    linux - python#同上
    linux.union(python)#并集 不修改原来集合
    linux | python #同上
    linux.symmetric_different(python)#对称 差集 互相都不在列表内的元素



    #增
    update() 合并
    add() 增加
    copy() 浅复制




    #删
    clear()
    discard(‘XXX’) 
    pop() #随机删除
    remove(‘XXX’) #XX元素不存在，会报错




    #改
    difference_update() #差集取出来覆盖前面集合的值，少用




    #查
    issubset() #判断是否子集
    issupset() #判断是否父集合
    isdisjoin()#两个集合完全不一样返回真


18、字符串操作

    capitalize() 首字母大写
    casefold()   全部小写 ，用于判断前转换
    center(长度，’填充值’)  置中
    count(‘x’,从第几个开始统计,结尾) 统计一个字符出现的次数
    end//startswith(‘xx') 以xx结尾 返回T or F
    expendtabs()  设置tab长度
    find(‘xxx’,从头，尾)              查找xxx字符，返回第一个值索引值，找不到返回-1
    
    format(name=‘’,age='' )            格式化输出
    把字符串大括号的值替换{0}{1} 
                                            {name}{age}
    
    format_map({‘’:'’})                   传入字典
    Isalnum()           判断所有字符是否数字加英文
    Isdecimal()        判断是否十进制数字
    Isalpha().           判断全部是否是字母
    Isidentifier()       判断是否是合法变量名
    Islower().           是否小写
    Isupper().                大写
    Isnumeric()        是否是全数字，返回T or F
    Isprintable()       是否可打印
    isspace().           是否空格
    Istitle()                是不是英文标题 ，全单词首字母大写
    Join()                  ‘隔开的符号’.join(a) 转换成字符串
    ljust(50,’-‘)            左对齐，不够用 - 补充
    rjust(50,’-‘)           右对齐
    rfind(‘xxx’)            从右边开始查找
    lstrip()                    只脱左边空格制表符换行或指定
    Swapcase()            大小写互换
    translate()     #创建翻译表    
    IN= ‘abcde’.  OUT = ‘12345’
    Tran_tab = str.maketrans(IN,OUT)
    
    Print(name.translate(Tran_tab))
                           
    zfill(50)       填充50个0
    replace(’name’,’NAME’, 次数)       把原来的值替换

19、字符编码转换

ASCII 英文

GB2312 1980

GBK    1995
GB18030     
unicode   1990
        Utf - 8

——————————————————

JK日语翻译——> unicode（utf-16）——>GBK

         Decode解码成                Encode编码 
 ——————————————————


指定编码方法

    #!/usr/bin/python
    # -*- utf-8 -*-

XXX.decode(‘UTF-8’) 现在的编码————>变成了unicode u’/xxx/xxx’
XXX.encode(‘BGK’) 要变成的编码————>变成GBK

[XXX] 显示16进制模式，用列表框住
                    
len(XXX).  Utf8 占6个字节
len(XXX)  unicode 占2个字符
len(XXX). GBK 占4个字节

ASCII 127个  7个比特位—USA

扩展ASCII 256个 8个比特位—拉丁

中文扩展ASCII 8（GB2312）

中文扩展ASCII 8（GBK）

Unicode ——两个字节：明文转换为二进制

UTF8：二进制对应的二进制

20、文件处理

（1）读取 ：f =open(‘文件路径和文件名’)
                    
（2）
操作 ：

    f.read() #读取. 
    f.write() #写入 
    f.seek(0) #调整光标位置，按字节走
        f.seek(5, x).  #x = 0 从开始位置 x=1 从当前开始移动 x=2按最后的位置 #需要b模式
        #断点续传 
    f.tell() #查看光标位置
        read(n) #读取前n个字符 python3／      2读的是字节
        #光标从为止0开始读，读到最后，就结束


    #读：
    readline() 读取一行内容
       
    readlines() 读取每行内容，返回列表（包括\n 换行符）需要用.strip()去掉换行符
    for line in f:
        print (line.strip())
        line = ‘’.join([line.strip, ‘xxxxx\n’]) #拼接


    readable(). 返回布尔值


    #写：
    write()
     在开头需要设置为可写对象
    f = open(’test.txt’, mode=‘rw', encoding=‘xxx’)
    
    
    f = open(’test.txt’, mode=‘aw', encoding=‘xxx’) #a 是追加模式，在光标末端追加
                                                    #x 跟 w 模式一样,但是有相同文件时，会报错
                                                    
    #可读可写
    r+  ：光标处追加写入功能
    w+ ：覆盖写入，可以用seek调整
    a+  ：追加到最后
    b : 通过字节数据类型 
    wb,ab : 操作对象是字节，需要encoding!!!

    f.write(‘XXXX’). #覆盖为XXXX 。如果文件不存在，直接创建

    f.flush() #刷新，马上把缓存内容已到硬盘


    #进度条
    import sys, time
    
    for i in range(100)
    
        s=“\r%d%% %s” % (i,”#”*i) #两个百分号打印一个百分号.  \r代表从头开始覆盖
        sys.stdout.write(‘#’)
        Sleep.time(0.25)
        sys.stdout.flush()


（3）
关闭 ：f.close()



with open(‘文件名’) as f:        #= f = open(’文件名’)
    f.read()

#结束就不用close()了



(4)文件操作
Import os 
os.rename(‘xxx’,’xxx_bak’)
os.rename(‘xxx_test’,’xxx')

