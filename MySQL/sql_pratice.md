
# 一、表关系

![image](https://github.com/MMingLeung/Markdown-Picture/blob/master/tables.png?raw=true)


# 二、操作表

### 1、创建表

	create table class(cid int not null auto_incremnet primary key,
	                    caption varchar(32) not null)engine=innodb default charset=utf8;
	
	create table student(sid int not null auto_increment primary key,
	                      sname varchar(32) not null,
	                      gender char(10) not null,
	                      class_id int,
	                      constraint fk_student_class foreign key (class_id) references class(cid)
	                      )engine=innodb default charset=utf8;
	
	create table teacher(tid int not null auto_increment primary key,
	                      tname varchar(32) not null)engine=innodb default charset=utf8; 
	
	create table course(cid int not null auto_incremnet primary key,
	                     cname varchar(32) not null,
	                      teacher_id int,
	                      constraint fk_course_teacher foreign key (teacher_id) renferences teacher(tid))
	                       engine=innodb default charset=utf8;
	
	create table score(sid int not null auto_increment primary key,
	                    student_id int,
	                    corse_id int,
	                    number int,
	                    constraint fk_score_course foreign key(corse_id) references course(cid),
	                    constraint fk_score_studnet foreign key(student_id) references student(tid)
	                    )engine=innodb default charset=utf8;



### 2、查询“生物”课程比“物理”课程成绩高的所有学生的学号；


	select * from 
	(select student_id,number from score 
	left join 
	course on score.corse_id = course.cid where corse_id=1) as A 
	left join 
	(select student_id,number from score 
	left join 
	course on score.corse_id = course.cid where corse_id=3) as B on A.student_id = B.student_id where A.number > B.number

​	

### 3、查询平均成绩大于60分的同学的学号和平均成绩； 

	select student_id,avg(number) from score group by student_id having avg(number) > 60;

	-- 再加上学生姓名
	SELECT B.studnet_id,student.sname,B.avgnum FROM 
	(select student_id,avg(number) as avgnum from score 
	group by student_id having avg(number) > 60）as B 
	LEFT JOIN studnet ON B.student_id=studnet.sid;

### 4、查询所有同学的学号、姓名、选课数、总成绩；

	select student_id,student.sname,count(corse_id),sum(number) from score 
	left join 
	student on score.student_id=student.sid group by student_id

### 5、查询姓“M”的老师的个数；

	select count(tname),tname from teacher where tname like 'M%' group by tid;

### 6、查询没学过“Alice”老师课的同学的学号、姓名；

	SELECT * from student where sid not in
	(SELECT sid FROM score where corse_id in 
	(select course.cid from course left join teacher on teacher.tid=course.teacher_id where teacher.tname="Alice"));


### 7、查询学过“1”并且也学过编号“2”课程的同学的学号、姓名；

	 select student_id,student.sname from score 
	left join 
	student on score.student_id=student.sid 
	where corse_id =1 or corse_id=2 group by student_id having count(corse_id) > 1;


### 8、查询学过“Charlie”老师所教的所有课的同学的学号、姓名；

	select A.student_id,student.sname from
	(select * from score where score.corse_id =
		(select cid from course 
		left join teacher on teacher.tid=course.cid wh ere teacher.tname="Charlie"))as A 
	left join student on A.student_id =student.sid


### 9、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；

	select * from
	(select A.student_id,A.number as c1,B.number as c2 from (select * from score where score.corse_id=1) as A 
	INNER join
	(select * from score where score.corse_id=2) as B on A.student_id=B.student_id where A.number<B.number) As C 
	LEFT JOIN student on student.sid = C.student_id;


### 10、查询有课程成绩小于60分的同学的学号、姓名；

	-- 新知识点: DISTINCT 效率不高

	select student_id from score left join student on student.sid=score.stude
	nt_id where number < 60 group by student_id;
	
	select DISTINCT student_id from score 
	left join 
	student on student.sid=score.student_id where number < 60 ;


### 11、查询没有学全所有课的同学的学号、姓名；

	-- count(主键或者1) 效率高
	select student_id,count(corse_id) from score group by 
	student_id having count(corse_id) < (select count(1) from course);


### 12、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名；

	select student_id from score where corse_id in 
	(select corse_id from score where student_id = 1) and student_id !=1 group by student_id;

### 13、查询至少学过学号为“1”同学所选课程的其他同学学号和姓名；

	select student_id,count(1) from score where corse_id in 
	(select corse_id from score where student_id = 1) and student_id !=1 
	group by student_id having count(1) > (select count(course_id) from score where student_id = 1);


### 14、查询和“2”号的同学学习的课程完全相同的其他同学学号和姓名；

	-- 1、获取与2同学选课个数一样的同学
	select count(1) from score where student_id =2;
	
	select student_id,count(1) from score where student_id != 2 group by student_id having count(1) = (select count(1) from score where student_id =2);
	
	-- 2、再找课程编号在2号同学的课程编号里面的同学
	
	select student_id from score where student_id in 
	(select student_id from score where student_id != 2 group by student_id having count(1) = 
		(select count(1) from score where student_id =2)) 
	and corse_id in (select corse_id from score where student_id =2) group by student_id having
	count(1) = (select count(1) from score where student_id =2) ;


### 15、删除学习“Mike”老师课的SC表记录；
	delete from score where course_id in 
	(select cid from course 
	left join 
	teacher on course.teacher_id = teacher.tid where teacher.tname = "Mike")


### 16、向SC表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“2”课程的同学学号；②插入“2”号课程的平均成绩； 


	-- 没有上过编号“002”课程的同学学号
	select student_id,2,(select avg(number) from score where corse_id=2) from score where corse_id != 2 group by student_id;
	
	INSERT INTO score (student_id, number, courser_id)
		SELECT S.B, S.A, S.C FROM 
		   (SELECT avg(number) AS A,
			(SELECT student_id FROM score WHERE student_id not in 
			 (SELECT student_id FROM score WHERE courser_id = 2)) AS B ,
		2 AS C FROM score WHERE courser_id = 2 GROUP BY courser_id
	) as S


### 17、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 学生ID,语文,数学,英语,有效课程数,有效平均分；

	SELECT student_id,
		(SELECT number from score as s2 WHERE s2.student_id = s1.student_id 		and courser_id = 1) as biology, 
		(SELECT number from score as s3 WHERE s3.student_id = s1.student_id 		and courser_id = 2) as physics, 
		(SELECT number from score as s4 WHERE s4.student_id = s1.student_id 		and courser_id = 3) as math,
		avg(number) as av
		FROM score as s1 GROUP BY student_id ORDER BY av ASC

### 18、查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；

	select corse_id,max(number),min(number) from score group by corse_id;


	-- 如果最低分小于50显示00用case when then else end
	select corse_id,max(number),case when min(number)<50 then 00 else min(num
	ber) end from score group by corse_id;

### 19、按各科平均成绩从低到高和及格率的百分数从高到低顺序；

	-- 先求小于60的人显示0，大于则显示1，增加一列1，group by corse_id之后对case求和除以人数
	select corse_id,avg(number),sum(case when number<60 then 0 else 1 end)/su
	m(1) as g from score group by corse_id order by avg(number) asc,g desc;

### 20、课程平均分从高到低显示（显示任课老师）；

	select score.corse_id,avg(number),teacher.tname from score 
	left join 
	course on score.corse_id = course.cid 
	left join 
	teacher on teacher.tid=course.teacher_id group by score.corse_id;

三运算：a = 111 if 1 == 1 else 110

### 21、查询各科成绩前三名比第四名大的记录:(不考虑成绩并列情况) 

分组避免重复分数
	SELECT
	corse_id,
	(select number from score where corse_id=s1.corse_id group by number order by number  desc limit 0,1) ,
	(select number from score where corse_id=s1.corse_id group by number order by number  desc limit 1,1) ,
	(select number from score where corse_id=s1.corse_id group by number order by number  desc limit 2,1)
	from score as s1 GROUP BY corse_id;
	
	select * from
	(
	SELECT
	student_id,
	corse_id,
	number,
	(select number from score as s2 where corse_id=s1.corse_id group by s2.number order by s2.number  desc limit 0,1),
	(select number from score as s2 where corse_id=s1.corse_id group by s2.number order by s2.number  desc limit 1,1),
	(select number from score as s2 where corse_id=s1.corse_id group by s2.number order by s2.number  desc limit 2,1) as cc
	from score as s1
	) AS B where B.number > B.cc

### 22、查询每门课程被选修的学生数；

	select corse_id,count(1) from score group by score.corse_id;

### 23、查询出只选修了一门课程的全部学生的学号和姓名；

	select student_id,count(corse_id) from score group by student_id;

### 24、查询男生、女生的人数；

	select student_id,count(corse_id) from score group by student_id;

### 25、查询“M”开头的学生名单；

	select sname,count(1) from student where sname like 'M%' group by sname;

### 26、查询同名同姓学生名单，并统计同名人数；

	select sname,count(1) from student group by sname;

### 27、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；

	select corse_id,avg(number) from score group by corse_id order by avg(num ber) asc ,corse_id desc;


### 28、查询平均成绩大于85的所有学生的学号、姓名和平均成绩；

	select student_id,student.sname,avg(number) from score left join student on student.sid=score.student_id group by score.student_id having avg(number) > 85;


### 29、查询课程名称为“数学”，且分数低于60的学生姓名和分数；

	select * from score left join course on course.cid=score.corse_id where n umber < 60 and course.cname="math";


### 30、查询课程编号为3且课程成绩在80分以上的学生的学号和姓名； 

	select * from score left join student on student.sid=score.student_id where corse_id=3 and number > 80 


### 31、求选了课程的学生人数

	select student_id from score group by student_id ;

### 32、查询选修“Poppy”老师所授课程的学生中，成绩最高的学生姓名及其成绩；

	select student_id, student.sname ,corse_id, number from score left join student on student.sid=score.student_id where score.corse_id in (select course.cid from teacher left join course on course.teacher_id=teacher.tid where teacher.t name="Poppy") order by number desc limit 1;

### 33、查询各个课程及相应的选修人数；

	select corse_id,course.cname,count(1) from score left join course on cour se.cid=score.corse_id group by score.corse_id;


### 34、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；

	select student.id,corse_id,number from score as s1, score as s2 where s1.number=s2.number and s1.corse_id != s2.corse_id and s1.sid != s2.sid;

### 35、查询每门课程成绩最好的前两名；


	SELECT *
	FROM score as A
	--   B.number >= A.number 如果是COUNT(*)= 3 则代表这个人A.number排名在第3
	WHERE (SELECT COUNT(*)
	       FROM score as B
	       WHERE B.corse_id = A.corse_id
	       AND B.number >= A.number) <= 2
	ORDER BY A.corse_id, A.number DESC



### 36、检索至少选修两门课程的学生学号；

	select student_id,count(1) from score group by student_id having count(1) >2;


### 37、查询全部学生都选修的课程的课程号和课程名；

	select corse_id,count(1) from score 
	group by 
	score.corse_id having count( 1) = (select count(1) from student);

### 38、查询没学过“Alice”老师讲授的任一门课程的学生姓名；

	SELECT student_id FROM score where student_id not in
	(select student_id from score where corse_id in
	(select cid from course left join teacher on teacher.tid=course.teacher_id  where teacher.tname='Alice')
	 group by student_id)
	group by student_id;


### 39、查询两门以上不及格课程的同学的学号及其平均成绩；

	select score.sid,avg(score.number) from score 
	inner join
	(select student_id,count(1) from score where number < 60 
		group by student_id having count(1)>2) As A
	on score.sid = A.student_id GROUP BY score.sid


### 40、检索“1”课程分数小于60，按分数降序排列的同学学号；

	select student_id from score where score.corse_id=1 and score.number < 60 order by student_id desc 


### 41、删除“002”同学的“001”课程的成绩；

	delete from score where student_id=2 and corse_id=1;

