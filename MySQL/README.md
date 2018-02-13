# MySQL

### 用于管理文件的软件
服务端软件：socket服务端、本地文件操作、解析指令

客户端软件：socket客户端、发送指令、解析指令

DBMS： database manager system

     
学习：
安装服务端和客户端
连接
学习SQL语句规则；只在服务端做操作

类似软件：
关系型数据库：sqllite, db2, oracle, access, sql server, MySQL
非关系型数据库：MongoDB, redis

## 一、MySQL安装

windows:
可执行文件/压缩包

### 1、解压缩：
mysqld.exe服务端
mysql.exe客户端
          
### 2、安装：
进入数据库文件夹 >> mysql\bin\mysqld -install

### 3 、 初始化 --- 服务端
文件路径 mysqld --initialise-insecure


### 4、加入环境变量、启动mysqld
mysqld --skip-grant-tables(无密码登录模式)


	如果忘记密码：

	skip-grant-tables
	# 启动mysql服务
	net start mysqld
	cd C:\Program Files\MySQL\MySQL Server 5.7\bin
	mysql
	use mysql
	设置新密码
	update mysql.user set authentication_string=password('12345') where user='root' and Host = 'localhost';
	flush privileges;



	进入后如果报错：
	you must reset your password using alter user statement
	
	 1:  SET PASSWORD = PASSWORD(‘your new password‘);
	
	 2:  ALTER USER ‘root‘@‘localhost‘ PASSWORD EXPIRE NEVER;
	
	 3:  flush privileges;

### 5、基本命令

显示目录：show databases;

创建数据库：create database db1;创建名为db1的数据库

	mac : mysql/data 目录
	      使用find /usr/ -iname ‘数据库名字’
	      找出所在目录/usr//local/var/mysql/test1



### 6、windows服务

	路径\bin\mysqld —install
	路径\bin\mysqld —remove
	
	cmd >>:
	启动 net start MySQL
	停止 net stop MySQL

6.1 mac

	mysql.server start 
	mysql.server stop
	mysql.server restart


### 7、数据库结构
数据库（文件夹）

—表（文件）

—数据行（行）

### 8、连接

用户：root

创建：
create user '用户名’@'ip地址’  identified by ‘123456’;（用户需只能在某个ip登录）

create user '用户名’@‘192.168.1.%’  identified by ‘123456’;（用户需只能在某个ip段登录）

删除：drop user '用户名’@‘192.168.1.%’

修改用户： remove user '用户名’@‘192.168.1.%’; to ‘新用户名’@‘192.168.1.%’；；

修改密码：set password for '用户名’@‘192.168.1.%’ = Password(“新密码")

授权：
	只能操作某个数据库（取消授权：revoke from ）

	grant select,insert,update  on db1.*    to    ‘用户名’@‘ip’    
  
	权限          查、插入、更新    db1下所有文件        人

	    （all privileges 所有权限除了给别人授权功能）

进入：use mysql进入数据库

查看：show tables 查看表

查看表数据：select * from 表名;（*代表所有的列） 

## 二、MySQL规则
     
### 1、操作数据库：

创建  create database 数据库名字 default charset utf8; (设置编码)

查看  show databases;

删除  drop database 数据名;

改 ALTER TABLE `t_user` ADD unique(`username`);

### 2、操作表：

	创建 
	
	create table t1(id int, name char(10));
	
	create table t1(id int, name char(10)) default charset=utf8;
	
	create table t1(id int, name char(10)) engine=innodb default charset=utf8;
	
	引擎=myisam/innode(支持事务，原子性操作，出错后回滚，一定要)
	                
	create table t1(id int unsigned auto_increment primary key, (无符号， 自增,必需是主键（表示约束，不能为空且不重复））
	                  name char(10) null (可以为空)，
	                  sex char(10) not null default ‘保密’ (不为空)
	                    ) engine=innodb default charset=utf8;
	
	显示 show tables;
         
	清空
	delete from 表名字 , 但是之后增加数据，自增id会延续
	truncate table 表名字，自增id不延续
         
	删除 drop table 表名字


### 3、数据类型： 

数字：

1. int 整数

1. bigint 

1. tinyint 
  
1. float (小数不精准)

1. double (小数不精准)

1. decimal（总位数，小数点后最多有几位）（精准，以字符串保存）

字符串：

1. char(长度255）：当没占满是自动填充

1. varchar(长度255) ：不自动填充，但速度没有char快

1. PS：把定长的数据列往前放如:10001mike

1. text : 存放65535个字符
                               
时间：

1. DATE:YYYY-MM-DD

1. TIME:HH:MM:SS

1.  YEAR: YYYY

1. DATETIME:YYYY-MM-DD HH:MM:SS

枚举：
ENUM

集合：
	SET
	CREATE TABLE myset(
	        name varchar(40),
	        col SET(‘a’,’b’,’c’,’d’) #只能插入集合内的字符是我组合
	        )

* 上传文件：
文件存硬盘
数据库存路径



         

### 4、操作表内部数据：

增：

	插入 insert into t1 (id,name) values (1, ‘matt’)；
	        insert into t1 (name, age) values(‘a’, 12), (‘b’, 15)

	表1内容复制到表2 insert into tb2(id, name) select id,name from tb1;

查：

	查看 
	select * from 表名字 （*代表所有列）
	select id,name from tb1 where id >10 or name=‘xxxx’;
	select id,name from tb1 where id in(1,2,3); 在( )里面
	select id,name from tb1 where id not in(1,2,3); 不在( )里面
	select id,name from tb1 where id between 5 and 12; 闭区间
	
	先执行括号内的
	select id,name from tb1 where id in (select nid from tb2)
	
	通配符
	以a开头：a% , a_(后面跟一个字符)
	select id,name from tb1 where name like 'a%';

	分页 
	        limit
	        select * from tb1 limit 2;查看2条
	        select * from tb1 limit 0,10;查看前10条
	        select * from tb1 limit 10,10;查看第10条后面的10条
	
	        offset 从哪里开始
	        select * from tb1 limit 20 offset 20;
    
	#python分页
	
	page = input(“>>: “)
	page = int(page)
	page = (page - 1) * 10
	
	select * from tb2 limit page,10 
	
	#当输入1的时候： limit 0,10 代表第一页10条数据 
	#当输入2的时候： limit 10,10 代表第二页10条数据 

	排序 

        select * from tb1 order by id asc; 正序
        select * from tb1 order by id desc; 倒序
        select * from tb1 order by id desc limit 2;取后两行数据
        select * from tb1 order by id desc , name asc; 现根据id排序，如果重复再根据后面条件排序

	分组
       	select s_id,max(id) from user group by s_id;如果s_id一样，max(id)，显示id大的行。min(id)\count(id)计数

		*** 对于聚合函数的结果，进行二次筛选必须用having
		select count(id), max(id),p_id from tb1 group by p_id having count(id) > 2; 
		
		取别名 
		        select id,name as n from tb1 where id >10 or name=‘xxxx’
		
		增加一列 
		        select id,name,1 from tb1 where id >10 or name=‘xxxx’
		
		连表操作
        



		left join 左表全部显示(right join）
		
		
		innder join:join后有null ，就把这行隐藏。
		
		
	上下链表：
		union(自动去重)
		
		select sid,sname from student
		UNION All-- 不去重加ALL
		select * from teacher


删：

	删除 delete from t1 where id<(>,=,!=,>=,<=)6 （删除满足条件的数据）and xxxx /or xxxxx



改：

	修改 update t1 set name=‘aaa’ where id=1 
        



### 5、外键：

跟另外一张表的id创建关系

	create table user_info(
	uid int auto_increment primary key,
	name not null varchar(32),
	department_id int,
	constraint fk_user_depar foreign key (department_id ) references department(id)
	)engine=innodb default charset=utf8;
	
	create table department(
	        id int auto_increment primary key;
	        name not null char(15)    
	)engine=innodb default charset=utf8;


 
补充知识：
1、一个表只能有一个主键
2、一个主键可以是多列组成

	create table t1 (
	    id int not null auto_incremnet ,
	    pid int , 
	    primary key (nid, pid)
	)engine=innodb default charset=utf8;


### 6、自增列初始值

（1）、show create table tb1 \G(竖看)

（2）、AUTO_INCREMENT=N 说明下一行的id是N

（3）、alter table tb1 auto_increment=2 设置后
             下一行的id由2开始
（4）、desc tb1 查看每个字段的设置

### 7、自增步长

MySQL 基于会话（登录终端）级别

	show session variables like 'auto_inc%’; 查看步长
	set session auto_increment=2;  设置步长为2
	set session offset=2;  设置启始值为2
	
	             基于全局级别（少用）
	             set global auto_increment=2

SQL server 基于表级别

### 8、唯一索引（加速查找）

	create table 1 (
	        id int …,
	        num int,
	        xxx int
	        unique uq1(num,xxx) # num,xxx联合唯一（两个值不能完全一样）
	)
	
	约束不能重复（可以为空），加速查找

### 9、外键变种

（1）、用户表和部门表
            多个人可以在一个部门

（2）、用户表和软件功能1表 
            一个人可以多个功能1（外键+唯一，就能解决，实现一对一）

方式一：
主管才有高级功能
id
username
usertype  
password
1
a(主管才有密码)
1
111
2
b
2

 
方式二：
外键user_id是user表的外键+唯一索引
id
user_id 
password
1
1
111222
2



（3）、多对多
例子1：
用户表（交友软件）
ID
name
gender
1
a
male
2
b
female
3
c
male
 
交友情况记录
两个外键 user1 user2对应用户表的ID，可以重复，双向多对多
id
user1
user2
1
1
2
2
2
3
3
1
3

例子2:
用户表
ID
name
1
a
2
b
3
c
主机表
id
name_server
1
s_1
2
s_2
3
s_3
用户主机关系表
联合唯一，保证用户跟主机不重复
id
 user_id
server_id
1
1
1
2
1
2
3
3
1


* 备份：（全部）mysqldump -uroot -p --databases db2 > /Users/mingleung/Documents/db2.sql 
          
         （表结构） mysqldump -uroot -d -p db2 > /Users/mingleung/Documents/db2.sql
                                        
     
* 还原 （自行先创建db2，再执行）：mysql -uroot -p db2 < db2.sql 


### 10、临时表

	select id from (select * from score where number > 60 ) as B;


## 三、navicat使用

1、创建
2、新建查询
3、转储SQL文件

## 四、练习

1、-- 是注释！



## 五、pymysql模块

### 1、安装

pip install mysql

### 2、连接

(错误方法，sql注入)

	conn = pymysql.connect(host="localhost", user="root", password="qwert",database="db2")
	cursor = conn.cursor() #连接
	sql =  "select * from userinfo where username=%s and password=%s" % (username,password)
	cursor.execute(sql ) #游标
	result = cursor.fetchone() #只拿第一条
	cursor.close()  #关闭
	conn.close()


### 3、提交

	增删改一样
	import pymysql
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db2")
	cursor = conn.cursor()
	sql = "insert into pytest(username,password) VALUES ('Caroline','123')"
	cursor.execute(sql)
	conn.commit()

	批量
	import pymysql
	
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db2")
	cursor = conn.cursor()
	sql = "insert into pytest(username,password) VALUES(%s, %s) "
	cursor.executemany(sql,[("a","1"),("b","2"),("c","3")])
	conn.commit()
	print(cursor.lastrowid) # 最后插入的数据的自增ID


	查
	
	import pymysql
	
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db2")
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) #fetch获得的数据改为字典形式
	sql = "insert into pytest(username,password) VALUES(%s, %s) "
	sql1= "select * from pytest"
	# r 是受影响的行数
	#r = cursor.executemany(sql,[("a","1"),("b","2"),("c","3")])
	#print(r)
	cursor.execute(sql1)
	# conn.commit()
	result = cursor.fetchone()
	print(result)
	result = cursor.fetchall()
	print(result)


## 六、用户权限管理设计方案
基于角色：
角色表：
1、IT部门员工
2、咨询员工
3、IT主管

权限表：
1、查看
2、修改

角色权限表：
1 1 
2 1 
3 1
3 2 

用户表：
id username pwd role_id （角色id） 

## 七、视图

给某个查询语句设置别名，方便使用

100个SQL语句要用到临时表：

SELECT * FROM tb1 WHERE id > 0;  起别名s1

SELECT ... FROM s1;

创建方法：create view as v1 select * from student;

删除：drop view v1;

如果在student 增加数据视图v1也会相应增加吗？会，动态读取，不能修改。

## 八、触发器

注册时，用户表增加一条数据，日志表增加一条用户所有信息

1、每次望t1插入数据，tb2也插入一条

	CREATE TRIGER tr1 BEFORE INSERT ON t1 FOR EACH ROW
	BEGIN 
	INSERT INTO tb2 .....
	END
	
	BEFORE AFTER
	            X
	INSERT UPDATE DELETE



创建触发器执行前把终止符; 改为其他 

	delimiter //
	create trigger t1 before INSERT on userinfo for EACH ROW
	BEGIN
	    INSERT into permission(per_name) VALUE (1111);
	END
	
	create trigger t1 before INSERT on userinfo for EACH ROW
	BEGIN
	    INSERT into permission(per_name) VALUE (NEW.name);   -- new代表新插入的信息   old代表老数据（删除、更新）
	END
	delimiter ;


## 九、函数(性能低)

内置函数：

	select CURDATE();
	select SUM();
	select CHAR_LENGTH("123");求字符长度
	select CONCAT("a","b","c");字符串拼接
	select DATE_FORMAT('2010-10-10 22:33:34', '%Y');时间格式化
	
	select DATE_FORMAT('2010-10-10 22:33:34', '%Y');时间格式化
	例子：博客文章按年份月份归类
	select ctime,count(1) from blog group by DATE_FORMAT(ctime,"%Y-%m")

自定义函数：

	delimiter \\
	create function f1(
	i1 int,
	i2 int)
	returns int
	BEGIN
	  --不能写select语句
	  declare num int;
	  set num = i1 +i2 ;
	  return (num);
	END \\
	delimiter;
	
	--调用
	select f1(1,199);

## 十、存储过程

保存在MySQL上的一个别名 --- 大量SQL语句
别名()
用于替代sql语句

	--创建
	delimiter //
	create PROCEDURE p1()
	BEGIN
	    select * from permission;
	    INSERT into permission(per_name) VALUEs("yayaya");
	END //
	delimiter ;

	--调用
	call p1()
	
	--传参数（in,out,inout）
	delimiter //
	create PROCEDURE p2(
	in n1 int,
	in n2 int
	)
	BEGIN
	    select * from permission where id > n1;
	END //
	delimiter ;
	
	--使用
	call p2(1,2)

	--返回值 out 传入参数后修改
	
	delimiter //
	create PROCEDURE p3(
	in n1 int,
	out n2 int
	)
	BEGIN
	    select * from permission where id > n1;
	    set n2 = 100000;
	END //
	delimiter ;
	
	set @v2=0;
	call p4(1,@v2);
	select @v2;


	#python
	import pymysql
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db_lianxi",charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) #fetch获得的数据改为字典形式
	cursor.callproc('p2',(3,2))
	conn.commit()
	result = cursor.fetchall()
	print(result)


	#python 获取in out 值
	import pymysql
	
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db_lianxi",charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) #fetch获得的数据改为字典形式
	
	cursor.callproc('p4',(2,2))
	conn.commit()
	result = cursor.fetchall()
	print(result)
	cursor.execute('select @_p4_0,@_p4_1')
	result1 = cursor.fetchall()
	print(result1)
	cursor.close()
	conn.close()


方式一：
mysql:存储过程
程序：调用存储过程

方式二：
程序：写SQL语句

方式三：
程序：类和对象

总结：1、可传参数 in out inout
          2、python可以调用


为什么有结果集和out返回值？用于标识存储过程的执行结果


事务：
	delimiter //
	create PROCEDURE p5(
	     out stat int
	)
	BEGIN
	  -- 1.声明如果出现异常执行  
	  { set stat = 1;
	    rollback;
	  }
	
	  开始事务
	       --A账户减去100
	       --B账户增加100
	       commit()
	  结束事务
	
	  set stat = 2;
	
	END //
	delimiter ;


	--例子
	delimiter //
	create PROCEDURE p5(
	     out stat int
	)
	
	BEGIN 
	 DECLARE exit handler for sqlexception
	 BEGIN 
	   --error
	   set stat = 1;
	   rollback;
	 END
	 
	 START TRANSACTION;
	select * from permission
	 COMMIT;
	
	 set stat = 2;
	
	END //
	delimiter ;


------------
	delimiter //
	create PROCEDURE p5(
	     out stat int
	)
	
	BEGIN
	 DECLARE exit handler for sqlexception
	 BEGIN
	   set stat = 1;
	   rollback;
	 END;
	
	 START TRANSACTION;
	        insert into permission(per_name) values("测试事务");
	 COMMIT;
	
	 set stat = 2;
	
	END //
	delimiter ;
	
	-- py中需要拿到@_p5_0就知道程序执行情况
	import pymysql

	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db_lianxi",charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) #fetch获得的数据改为字典形式
	
	cursor.callproc('p5')
	conn.commit()
	result = cursor.fetchall()
	print(result)
	cursor.execute('select @_p5_0')
	result1 = cursor.fetchall()
	print(result1)
	cursor.close()
	conn.close()


游标：

--基于游标

例子：

A表

id  num 

1    10

2    11

B表

id        num

1   A.id+A.num

delimiter //
create procedure p7()
begin
     declare row_id int;
     declare row_num varchar(50);
     declare temp int;
     declare done INT default FALSE;
     declare my_cursor CURSOR for select id,num from A;
     declare CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

     open my_cursor;
          xxoo:LOOP
               fetch my_cursor into row_id,row_num;
               if done then
                    leave xxoo;
               end if;
               set temp = row_id + row_num;
               insert into B(num) values(temp);
          end loop xxoo;
     close my_cursor;
end //
delimiter;



动态执行SQL防止注入：

delimiter //
create procedure p8(
     in tpl varchar(255);
     in arg int;
)
begin
     --预检测  sql语句合法性
     --格式化  tpl和arg格式化
     --执行sql
     set @arg = arg;
     PREPARE x FROM tpl;
     EXECUTE x USING @arg;
     DEALLOCATE prepare prod;
end //
delimiter;

call p7("select * from tb where id > ?", 9)


## 十一、索引

   文件数据的特殊结构，查询快，插入、更新和删除时慢

主键：不能为空+不能重复

唯一索引：可以为空+不能重复

联合索引（多列）：联合主键索引、联合唯一索引
  
### 1、创建、删除索引文件

普通索引：

	create index index_email on test(email);
	drop index

唯一索引：

	create unique index index_email on test(email);

联合索引：

	create unique index index_email on test(email,name);

### 2、索引种类：

hash索引：

索引表 数据转换成hash值和对应地址，数据位置可能跟原表不一致。

取单值速度快
取范围慢

btree索引：

把值转换成数字放到二叉树的各个位置

### 3、命中索引

	select * from test where email = '111@111.com';
	无法命中情况
	select * from test where email like '111@111.com' ;慢

	like '%aa%'：
     用户量少可以
     用户量大第三方工具：分析词语，各个词语编号，查询时先去文件找关系

	避免使用函数：
     reverse()翻转 #可以在python 中处理后再查询

	避免用or + 非索引的列
     select * from test where id = 1 or name = '1111';

	类型不一致(非主键)

	ORDER BY
     select name from test order by email 不走索引



### 4、覆盖索引

在特殊结构文件直接查出数据

	select email from test where email="111@111.com"

### 5、索引合并

合并使用多个单列索引

	select id,email from test where id =1 and email="111@111.com";


### 6、组合索引(效率大于合并索引)

	create unique index i1 on test(id,name,email);
	最左前缀匹配
	select id,email from test where id='1' and email="111@111.com";
	select id,email from test where name='A' and email="111@111.com";（不走索引）

### 7、注意事项

1. 尽量使用短索引create index i_1 on test(email(16));前十六个字符做索引
1. 使用count(1)
1. 连表条件类型一致 

### 8、时间

执行SQL的参考时间

执行计划 估算执行操作

	explain select * from test;



	type : all 全表< index 扫描特殊索引< range 等于where条件
			< index_range 合并索引< ref_or_null 查找一个值
			< eq_ref 连接主键或者unique类型< system/const  主键/常量

### 9、DBA的工作

慢日志：

1. 执行时间大于某个值
1. 未命中索引
1. 日志文件路径

配置:

     show variables like '%query%';
     set global slow_query_log=on;
     set global  long_query_time=5;
     show variables like '%queries%';
     set global  log_queries_not_using_indexes=on

指定配置文件：mysqld --default-file='D:\my.conf' 或者使用自己的配置文件my-default.ini 修改完需要重启服务 

	set global slow_query_log=on;
	set global log_queries_not_using_indexes=on;
	set global long_query_time=5;

### 10、分页查看

	select * from test limit 0,10;
	去索引表查select * from test where id in (select id from test limit 9999,10;)
	方案：
	记录当前页面最大或最小的id
	下翻页select * from test where id > 上一页最大一条数据的id limit 10;
	上翻页select * from test where id < 上一页最小一条数据的id order by id desc limit 10;

	比如要看194页，当前是191，取出191的limit 30,然后倒叙排的第一条数据就是193最后一条数据，就可以用上述方法查询
	select * from test where id in (select * from (select * from test where id >max_id limit 30) order by id desc limit 10);

## 十二、面向对象回顾

面向对象：数据和逻辑组合在一起

函数式编程：数据和逻辑分离

1. 提取相同的属性、行为  
1. 分类
1. 建立模板

## 十三、pymysql

	import pymysql
	#连接
	conn = pymysql.connect(host="localhost", user="root", password="qwert", database="db2")
	#获取游标
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor) #fetch获得的数据改为字典形式
	#sql语句	
	sql = "insert into pytest(username,password) VALUES(%s, %s) "
	sql1= "select * from pytest"
	#r 是受影响的行数
	#r = cursor.executemany(sql,[("a","1"),("b","2"),("c","3")])
	#print(r)
	#执行
	cursor.execute(sql1)
	# conn.commit() #修改增加需要commit
	result = cursor.fetchone()
	print(result)
	
	result = cursor.fetchall()
	print(result)
	
	#练习
	#! -*- coding:utf8 -*-
	import pymysql

	username = input(">>: ")
	password = input(">>: ")
	conn = pymysql.connect(host="localhost", user="root", password='qwert', database='db_lianxi')
	cursor = conn.cursor()
	sql = "select * from userinfo where username=%s and password=%s"
	cursor.execute(sql,(username,password))
	
	result = cursor.fetchone()
	print(result)
	user_id = result[0]
	print(user_id)
	if result:
	    sql1 = "select permission.per_name from user_per " \
	           "left join userinfo on userinfo.id=user_per.user_id " \
	           "left join permission on permission.id=user_per.per_id " \
	           "where user_id=%s"
	    cursor.execute(sql1,user_id)
	    result = cursor.fetchall()
	    print(result)

## 十四、ORM框架object relation mapping：SQLAlchemy

### 1、作用

提供简单的规则

自动转换成SQL语句

### 2、DB first ：手动创建数据库和表--> ORM -->自动生成累

### 3、code first: 手动创建类、数据库   --> ORM --> 手动创建表（SQLAlchemy ）

### 4、功能

创建数据库表

连接数据库（pymysql）

类转换成SQL语句


操作数据表
增
删
改
查

	#! -*-coding:utf8-*-
	import pymysql
	from sqlalchemy.ext.declarative import declarative_base
	from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker,relationship
	
	Base = declarative_base()
	
	class Users(Base):
	    __tablename__ = 'users'
	    id = Column (Integer, primary_key=True, autoincrement=True)
	    name = Column(String(32), nullable=True, index = True)
	    email = Column(String(16))
	    dep_id = Column(Integer, ForeignKey("department.id"))
	
	    #创建关系，查询更简单，不用手动连表         backref 给Department用的
	    user_dep = relationship("Department", backref="dep_back")
	
	    __tablename__args__  = (
	    UniqueConstraint("id", "name", name="unique_id_name" ),
	        Index("ix_name_email", "name", "email"),
	    )
	
	class Department(Base):
	    __tablename__ = 'department'
	    id = Column(Integer, primary_key=True, autoincrement=True)
	    name = Column(String(32),nullable=False, index=True)
	
	def create_db():
	    engine = create_engine("mysql+pymysql://root:qwert@localhost:3306/orm?charset=utf8", max_overflow=5)
	    Base.metadata.create_all(engine)
	
	def drop_db():
	    engine = create_engine("mysql+pymysql://root:qwert@localhost:3306/orm?charset=utf8", max_overflow=5)
	    Base.metadata.drop_db(engine)
	
	engine = create_engine("mysql+pymysql://root:qwert@localhost:3306/orm?charset=utf8", max_overflow=5)
	#-------------增--------------
	Session = sessionmaker(bind=engine)
	session = Session()
	# obj1 = [Users(name='matt',email='matt@163.com',dep_id=1),
	#         Users(name='Jack', email='Jack@163.com', dep_id=1)]
	# session.add_all(obj1)
	# session.commit()
	# session.close()
	
	#-------------查--------------
	# users_list = session.query(Users).all()
	# for row in users_list:
	#     print(row.id, row.name)
	
	#等于SELECT id FROM users where id > 2
	# users_list = session.query(Users.id).filter(Users.id > 2)
	# for row in users_list:
	#     print(row.id)
	
	#分组、排序、连表、通配符、子查询、limit、union、原生sql
	
	#______条件______
	
	#filter_by(name="matt") 内部转换成表达式
	# users_list = session.query(Users.id).filter_by(name="matt").all()
	#
	# #filter默认and
	# users_list = session.query(Users.id).filter(Users.id > 2, Users.name=='matt').all()
	# users_list = session.query(Users.id).filter(Users.id.in_([1,2,3]) , Users.name=='matt').all()
	# #不在1 2 3里
	# users_list = session.query(Users.id).filter(~Users.id.in_([1,2,3]) , Users.name=='matt').all()
	# users_list = session.query(Users.id).filter(Users.id.in_(session.query(Users.id).filter(Users.id > 2)) , Users.name=='matt').all()
	#
	# from sqlalchemy import and_, or_
	# users_list = session.query(Users.id).filter(or_(Users.id.in_([1,2,3]) , Users.name=='matt')).all()
	#
	# users_list = session.query(Users.id).filter(
	#     or_(
	#         Users.id < 2  , and_(Users.name.like ('%m'),  Users.name.like ('%a')))
	#     ).all()
	#
	# #______通配符______
	# users_list = session.query(Users.id).filter(Users.name.like("_a")).all()
	# users_list = session.query(Users.id).filter(~Users.name.like("_a")).all()
	#
	# #______分页______
	# users_list = session.query(Users.id)[1:2]
	#
	# #______排序______
	# users_list = session.query(Users.id).order_by(Users.name.desc()).all()
	# users_list = session.query(Users.id).order_by(Users.name.desc(), Users.id.asc()).all()
	#
	# #______分组______
	# from sqlalchemy.sql import func
	# users_list = session.query(Users.id).group_by(Users.name).all()
	# users_list = session.query(func.sum(Users.id),
	#                            func.max(Users.id),
	#                            func.min(Users.id)
	#                            ).group_by(Users.name).all()
	# users_list = session.query(func.sum(Users.id),
	#                            func.max(Users.id),
	#                            func.min(Users.id)
	#                            ).group_by(Users.name).having(func.min(Users.id) > 2).all()
	#
	# #______连表______
	# #SELECT * FROM users inner join department on users.dep_id=department.id
	# users_list = session.query(Users, Department).filter(Users.dep_id==Department.id)
	# #inner join
	# users_list = session.query(Users).join(Department).all()
	# #left join
	# users_list = session.query(Users).join(Department,isouter=True).all()
	# #right join
	# users_list = session.query(Department).join(Users,isouter=True).all()
	#
	# #______组合______
	# users_list = session.query(Users).union(Department).all()
	# users_list = session.query(Users).union_all(Department).all()
	#
	# #______临时表子查询______
	#
	# #SELECT * FROM (select * from tb) as B;
	# users_list = session.query(Users).filter(Users.id > 2).subquery()
	# res = session.query(users_list).all()
	#
	# #SELECT id,(SELECT * FROM tb2 where tb2.id=1) FROM tb1;
	# users_list = session.query(Department.id, session.query(Users).filter(Users.dep_id==Department.id).as_scalar()).all()
	#
	
	
	
	
	
	
	#-------------改--------------
	#session.query(Users.id).filter(Users.id > 0).update({"email":'test@gmail.com'})
	
	#在原来基础上加上任意值, synchronize_session=False字符串类型  “evaluate”数字类型
	# session.query(Users.id).filter(Users.id > 0).update({Users.name:Users.name + "X"},
	#                                                     synchronize_session=False)
	#
	# session.commit()
	# session.close()
	
	
	#-------------删----------------
	# users_list = session.query(Users.id).filter(Users.id > 2).delete()
	# for row in users_list:
	#     print(row.id)
	
	
	
	#问题1 ： 获取用户信息和关联的部门名称
	# users_list = session.query(Users, Department).join(Department, isouter=True).all()
	# for row in users_list:
	#     print(row[0].id,row[0].name,row[0].dep_id,row[1].name)
	
	#方法二
	#不加all() 就是迭代器 == fetchone()
	# users_list = session.query(Users)
	# for row in users_list:
	#     # 建立关系relationship，正向操作，row.user_dep 获得对象（一行数据）
	#     print(row.id, row.name, row.user_dep.name)
	
	
	#问题2：获取用户部门
	# dep_list = session.query(Department)
	# for row in dep_list:
	#     print(row.id, row.name, session.query(Users).filter(Users.dep_id==row.id).all())
	
	#方法二  relationship 中的 backref 反向操作
	dep_list = session.query(Department)
	for row in dep_list:
	    print(row.id, row.name,row.dep_back)
	
	
	



