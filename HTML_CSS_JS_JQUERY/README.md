四、Javascript

操作HTML标签元素

1、ECMAScript

	* 核心ECMAScript
	* DOM --Document object model  文档对象模型
	* BOM --Browser object model   浏览器对象模型


2、基础规范
js是弱类型的语言

python 是强类型语言，不同类型不能相互操作，必须转换成同一类型。是动态语言，比如定义i = 12, （编译->解释运行）在解释运行时，才知道i = 12

3、数据类型

	基本数字类
	number 
	string
	boolean ： true = 1 false=0
	undefined
	数组[]
	
	引用数字类型
	     object
	
	4、类型转换
	parseInt 转换成int,必须是数字开头的。结果为NaN代表得不到结果
	
	5、运算符
	
	算数运算符
	自加++ 自减--
	       +=        -=
	
	逻辑运算符
	==   ！=   >   <    >=   <=
	与&&  或||  非 !
	完全等于===
	and       1 and 2 = 2
	or          1 or 2 = 1
	
	位运算符


	身份运算符
	a = 1
	b = a
	a is b
	
	关系运算符
	‘25’< '3' : true      2的ascii码<3    
	 '25' < 3     : '25'转换成数字 
	
	6、流程控制
	
		* 顺序执行
		* 选择执行
		* 循环语句


	（1）if else 
	if （表达式） {
	语句1;
	}else{
	语句2;
	}
	
	if （表达式） {
	语句1;
	}else if{
	语句2;
	}else{
	语句3;
	}
	
	（2）switch
	switch (表达式){
	case 值：语句一;
	case 值：语句二;
	case 值：语句三;
	default : 语句四;
	}
	
	（3）for 
	for (初始化；结束条件；增量）{
	 语句；
	}
	
	（4）while
	var i = 0;
	while (i<100){
	语句；
	}
	
	（5）try catch(3) finally
	try{
	语句1；
	}catch (e){
	语句2；
	}finally{
	语句3；
	}
	
	7、JS的对象
	7.1对象分类：
	数据对象：
	Number 
	
	String
	x.length --获取字符串长度
	x.toLowerCase() 转换小写
	x.toUpperCase() 转换大写
	x.trim()  去掉两边空格
	x.charAt(index) 通过位置获得字符
	x.indexOf('字符'， index(起始寻找位)) 通过字符查找位置，没有找到返回-1
	x.match(regexp) 返回匹配字符串的数据，没有返回null
	x.search(regexp) 返回匹配字符串的首字符位子
	x.substr( , ); 截断。参数：起始位置，长度
	x.substring(start, end) 截断。起始位置，结束位置。顾头不顾尾
	x.slice(start, end) 切片。顾头不顾尾
	x.replace(findstr, tostr) 替换。
	x.split('分隔符') 分割，返回数组对象。
	x.concat(addstr) 拼接。
	
	Boolean
	
	组合对象：
	Array
	创建： var arrname =[1,2,3];
	      var arrname = new Array(1,2,3);
	      var arrname = new Array(长度); arrname[0]=1; arrname[1]=2; 先创建后赋值      
	
	遍历：for (var i in arr){
	语句；}
	
	object数据类型，跟字典一样：d = {'name':'aa', 'age':'15'};
	     for (var i in d){
	          } // 遍历的是key
	 
	方法：
	var arr1 = [1,2,3,4]
	arr1.join(bystr) 拼接成字符串， str1 = arr1.join('-') --> '1-2-3-4'
	arr1.concat(str) 追加
	     var a = [1,2,3];
	     var b = [4,5,6];
	     alert(a.toString()); 返回1，2，3 object对象转换string
	     alert(b.toString());
	arr1.length 获取长度
	arr1.reverse() 翻转
	arr1.sort() 排序
	     function insort(a,b){
	          return a-b
	     }
	     sort(insort) ；按照insort处理排序,重写方法。
	arr1.slice(2,4) 切片，顾头不顾尾。
	arr1.splice(start, deletecount) 删除，参数：起始位置，删除个数 
	arr1.splice(start, 0 ，AddValue) 插入，参数：起始位置，0，插入到起始位
	
	push and pop:
	arr1.push() 输入放到最后
	arr1.pop() 弹出最后元素
	
	shift unshift 栈操作
	arr1.shift() 获得第一个元素
	arr1.unshift() 放入元素至首位


	总结：
	1、可以放入任意类型，没有限制
	2、长度随下标变化，用到多长就多长，可以跨越下标赋值。


	Math
	Math.abs() 绝对值
	exp() e的指数
	floor() 下舍
	log() 对数
	max(x,y)
	min(x,y)
	pow(x,y) x 的 y次幂
	random() 0~1之间浮点
	round() 四舍五入


	Date
	var date = new Date() //默认当前时间
	console.log(date)  // Mon Aug 14 2017 17:43:24 GMT+0800 (中国标准时间)
	console.log(date.toLocaleString()) //2017/8/14 下午5:43:24  时间转换成string
	date.toUTCString() //Sun, 03 Nov 2013 04:42:23 GMT
	
	date.getDate() 获取当前多少号
	.getDay() 获取星期
	.getMonth() 获取月
	.getFullYear() 完整年份
	.getYear() 不完整年份
	.getHours() 
	.getMinutes()
	.getSeconds()
	.getMilliseconds() 毫秒
	.getTime() 1970/1/1至今的毫秒


​	
	高级对象：
	Object


	Error

​	
	Function（重点）
	function 函数名 (参数){
	          主体;
	           return 返回值;    
	          }
	
	//创建方式一
	function foo() {
	    console.log("ok");
	}
	var ret = foo()
	console.log(ret) //默认返回undefined
	//创建方式二（少用）
	var sayHello = new Function("name",“console.log(’hello’+’name’)”);
	var a = sayHello("aaa");
	console.log(a);
	
	//argument对象
	function add(a,b) {
	    console.log(arguments);
	    var sum = 0 
	     for (var i;i<argument){
	          sum +=      
	     }
	}
	function add(a,b) {
	    console.log(arguments);
	    var sum = 0
	
	    for (var i=0;i<arguments.length;i++){
	
	          sum += arguments[i]
	    }
	    console.log(sum)
	}


	//匿名函数    python:(lambada x,y:x+y)(1,2)
	var func = function (args){
	     return 'niming';
	}
	//正确方法，不用赋值，这样才能回收内存
	console.log((function (arg) {return arg;})(13123))


​	
​	
	RegExp

​	
	Global

​	
	实例化对象：

	var s = "hello";
	console.log(typeof s);
	
	// --------实例化对象 object 
	var s1 =new String("hello");
	console.log(typeof s1)


8、BOM对象（Brower object model）

8.1 Window对象方法

9、DOM
由对象组成:document, element, (文本，属性)

	// alert(123) // 提示

	// var ret = confirm(123)  // 提示 有确定取消按钮
	// console.log(ret)  // 返回true false
	
	// var ret = prompt("请输入数字")
	// console.log(ret)
	//用户输入数字作业 isNaN
	
	// open('http://www.baidu.com',"new","width=200,resizable=no,height=100") //打开窗口，参数:网址，窗口名字，窗口大小width=200,resizable=no,height=100
	
	// var s = setInterval(test, 100);  //设定定时器 参数：函数，毫秒
	// function test() {
	//    alert(100);
	// }
	// var s = setInterval(test, 1000);  //设定定时器 参数：函数，毫秒
	// clearInterval(s); //取消定时器
	
	// 走马灯练习作业
	
	//定时器需要定义一个函数，不然在函数体内会不断创建定时器，就清除不完
	//bug ：点击一次框 ,再点外面，再点进来，就生成两个定时器，就停止不了
	//
	// var ID;
	// function start() {
	//    if (ID ==undefined){
	//        test()
	//        ID = setInterval(test,1000);
	//    }
	// }
	//
	// function test() {
	//    var date = new Date();
	//    var timer = document.getElementById('timer');
	//    timer.value= date.toLocaleString();
	// }
	//
	// function end() {
	//    clearInterval(ID);
	//    ID = undefined;
	// }
	
	// 结点查找
	
	//直接寻找
	// document.getElementById();
	// document.getElementsByTagName();
	// document.getElementsByName();
	// document.getElementsByClassName();
	
	//显示null, 因为加载顺序问题。
	// var p = document.getElementsByTagName("p");
	// console.log(p[0]);
	//
	// var c1 = document.getElementsByClassName("c1");
	// console.log(c1);
	//
	// var c2 = document.getElementsByClassName("c2")[0];
	// console.log(c2);
	//
	// var a1 = document.getElementById("aa");
	// console.log(a1);
	
	//局部查找
	// var c1 = document.getElementsByClassName("c1")[0];
	// var p1 = c1.getElementsByTagName("p");
	// console.log(p1[0]);
	//
	// //导航结点属性
	// // parentElement //父节点
	// // children //所有子节点
	// // firstElementChild //第一个子标签
	// // lastElementChild //最后一个子标签
	// // nextElementSibling //下一个兄弟标签
	// // previousElementSibling //上一个兄弟
	// var pe = p1[0].parentElement;
	// console.log(pe.className);
	
	// 点击实现显示菜单，隐藏同级其他菜单。思路一：
	// function foo1(self) {
	//    var c1 = document.getElementsByClassName("c1");
	//    // console.log(c1);
	//    for (var i=0;i<c1.length;i++){
	//            c1[i].style.display="none";
	//    }
	//    self.nextElementSibling.style.display="block";
	// }
	
	/**
	* Created by Ming on 2017/8/15.
	*/
	
	// function foo() {
	//    // 创建标签
	//
	//    var ele = document.createElement("img");
	//    // 设置属性
	//    // ele.setAttribute(
	//    //    "src","https://www.google.com/logos/doodles/2017/mothers-day-2017-costa-rica-5706042934558720-2xa.gif");
	//
	//    // 动态DHTML
	//    ele.src="https://www.google.com/logos/doodles/2017/mothers-day-2017-costa-rica-5706042934558720-2xa.gif";
	//    //找父节点
	//    var container = document.getElementsByClassName("img")[0];
	//    // 添加子标签
	//    container.appendChild(ele);
	//   //.insertBefore(newnode, 某个结点) 放到结点之前
	// }
	//
	// function delete_p() {
	//    // 删除标签
	//    //找到父节点
	//    var container = document.getElementsByClassName("img")[0];
	//    //找到要删除的子节点
	//    ele_p = container.getElementsByTagName("p")[0];
	//    //删除
	//    container.removeChild(ele_p);
	//
	// }
	// function replace_p() {
	//    // 删除标签
	//    //找到父节点
	//    var container = document.getElementsByClassName("img")[0];
	//    //找到要替换的子节点
	//    ele_p = container.getElementsByTagName("p")[0];
	//    //新建一个标签
	//    var ele = document.createElement("img");
	//        ele.src="https://www.google.com/logos/doodles/2017/mothers-day-2017-costa-rica-5706042934558720-2xa.gif";
	//    //替换
	//    container.replaceChild(ele, ele_p);
	// }
	
	//结点属性操作
	
	// 查属性 document.getElementById("p1").getAttribute("id")
	// 改 document.getElementById("p1").setAttribute("id", "p2");
	// 查标签内容 document.getElementById("p2").innerText;
	// 改标签内容 document.getElementById("p2").innerText='lala';
	// 查标签所有内容（包括标签） document.getElementById("p1").innerHTML;
	// 改标签内容（可以加标签） document.getElementById("p1").innerHTML=“<i>qwqe<i>”;
	
	//select selectIndex 内容发生改变就触发
	// var eleS = document.getElementsByTagName('select')[0];
	// console.log(eleS);
	// function fooC(self) {
	//    alert(11);
	//    console.log(self); // self 是select标签
	//    console.log(self.selectedIndex);
	//    console.log(self[self.selectedIndex].innerText);//获取实际文本
	// }
	
	//改变css样式
	
	// var s = document.getElementsByTagName('span')[0]
	// s.style.fontSize="20px";
	
	//class 操作
	// var item2 = document.getElementsByClassName('item2')[0];
	// console.log(item2.className); //获取classname 字符串
	// console.log(item2.classList); //获取classname 列表
	// console.log(item2.classList.remove("head")); //删除class的值"head"


​	
	//模态对话框
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		    <style>
		        *{
		            margin: 0px;
		        }
		        .back{
		            width: 100%;
		            height: 1024px;
		            background-color: gold;
		        }
		        .shadow{
		
		            position: fixed;
		            top: 0px;
		            bottom: 0px;
		            left: 0px;
		            right: 0px;
		            background-color: #c2b192;
		            opacity: 0.6;
		            /*z-index: 1;*/
		        }
		        .model{
		
		            position: fixed;
		            width: 300px;
		            height: 400px;
		            background-color: #ff6d41;
		            /*z-index: 1000;*/
		            top:50%;
		            left:50%;
		            margin-left: -150px;
		            margin-top: -200px;
		            text-align: center;
		            /*line-height: 400px;*/
		        }
		        .ipt{
		            margin-top: 100px;
		        }
		        .hid{
		            display: none;
		        }
		    </style>
		</head>
		<body>
		
		<div class="back">
		    <button class="b1" onclick="foo()">start</button>
		</div>
		<div class="shadow hid"></div>
		<div class="model hid">
		
		    <div class="ipt">用户名：<input type="text">
		    <button class="ok" onclick="foo1()">ok</button>
		    </div>
		
		</div>
		
		</body>
		<script src="bom3.js"></script>
		</html>


		/**
		* Created by Ming on 2017/8/15.
		*/
		
		function foo(){
		    // document.getElementsByClassName("shadow")[0].classList.remove("hid");
		    // document.getElementsByClassName("model")[0].classList.remove("hid");
		    var hi = document.getElementsByClassName("hid");
		    for (var i=0;i<hi.length;i++){
		            console.log(hi[i]);
		            hi[i].classList.remove("hid");
		    }
		
		}
		
		function foo1() {
		    document.getElementsByClassName("shadow")[0].classList.add("hid");
		    document.getElementsByClassName("model")[0].classList.add("hid");
		
		}


​		
​		
		// 猜数字
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		</head>
		<body>
		<button onclick="cai()">1111</button>
		</body>
		<script src="caishuzi.js"></script>
		</html>
		
		/**
		* Created by Ming on 2017/8/15.
		*/
		
		var result = Math.round(Math.random()*100);
		console.log(result)
		function cai() {
		    var input = prompt("猜数字");
		    console.log(input);
		    if (isNaN(+input)) {
		        alert("请输入正确数字：");
		        console.log(input);
		        cai();
		    } else if (input < result) {
		        alert("请输入更大数字");
		        console.log(input);
		        cai();
		    }
		    else if (input > result) {
		        alert("请输入更小数字");
		        console.log(input);
		        cai();
		    }
		    else if (input == result) {
		        alert("6666666");
		    }
		
		}
		
		//跑马灯
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		    <style>
		        h1{
		            background-color: #ff6d41;
		            text-align: center;
		            line-height: 70px;
		        }
		    </style>
		</head>
		<body>
		
		<h1>欢迎光临！</h1>
		<button onclick="foo()">start</button>
		
		</body>
		<script src="paomadeng.js"></script>
		</html>
		
		/**
		* Created by Ming on 2017/8/16.
		*/
		
		// console.log(s);
		// for (var i=0;i<s.length;i++){
		//    console.log(s[i]);
		// }
		
		function foo() {
		    var s = document.getElementsByTagName("h1")[0].innerText;
		    var firstC = s.charAt(0);
		    var lastC = s.substring(1,s.length);
		    var newC =  lastC + firstC;
		    document.getElementsByTagName("h1")[0].innerText=newC;
		}
		var si = setInterval(foo,500);


​		
		/**
		* Created by Ming on 2017/8/16.
		*/
		function foo(self) {
		    self.value="";
		}
		function foo1(self) {
		    if (self.value.trim() == '') {
		        self.value = "请输入姓名";
		    }
		}
		
		// onchagne二级联动
		info = {"1":["11","12","13"],"2":["21","22","23"],"3":["31","32","33"]}
		
		var ele = document.getElementsByClassName("select")[0];
		var new_s = document.getElementsByClassName("new_select")[0];
		
		// 绑定事件和方法的另一种方法(this 可以直接取)：
		ele.onchange=function () {
		    var op = ele.children;
		    // console.log(op);
		
		    // 选中的索引
		    var idex = this.selectedIndex;
		
		    // option的文本
		    var key = op[idex].innerText;
		    var list_value = info[key];
		    console.log(list_value);
		
		    //选择前先删除已有内容一：
		    // var new_s_c = new_s.children;
		    // var l_new_s_c = new_s_c.length;
		    // for(var j=0;j<l_new_s_c;j++){
		    //        new_s.removeChild(new_s_c[0]);
		    // }
		    //二：清空select子元素
		    new_s.options.length=0;
		
		    // 添加内容
		    for (var i=0;i<list_value.length;i++){
		
		        var new_op = document.createElement("option");
		
		        new_op.innerText=list_value[i];
		        console.log(new_op);
		        new_s.appendChild(new_op);
		    }
		
		};
		
		var f = document.getElementsByTagName("form")[0];
		// 事件保存的对象e
		f.onsubmit = function (e) {
		    alert(123);
		
		    //阻止默认事件发生
		    // return false;
		
		    //阻止事件发生
		    // e.preventDefault();
		};
		
		//选中触发onselect
		var input1 = document.getElementsByClassName("input1")[0];
		input1.onselect=function () {
		    alert(123);
		};
		
		//盒子绑定事件
		var out = document.getElementsByClassName("outer")[0];
		out.onclick=function () {
		    alert(123);
		};
		//先执行自己的事件，再执行外面事件，事件传播
		var inn = document.getElementsByClassName("inner")[0];
		inn.onclick=function (e) {
		    alert(345);
		    //防止事件传播
		    e.stopPropagation();
		};
		
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		    <style>
		        .outer{
		            width:200px;
		            height: 200px;
		            background-color: #ff6d41;
		        }
		        .inner{
		            width:100px;
		            height: 100px;
		            background-color: #62ff80;
		        }
		    </style>
		</head>
		<body>
		<input type="text" onfocus="foo(this)" value="请输入姓名" onblur="foo1(this)">
		
		<div><select name="" id="" class="select">
		    <option value="1">1</option>
		    <option value="2">2</option>
		    <option value="3">3</option>
		</select>
		<div class="num"></div>
		<select name="" class="new_select">
		
		</select>
		</div>
		<!--onsubmit先触发，后触发submit-->
		<form action="" method="post" id="form">
		    用户名：<p><input type="text" name="user"></p>
		    密码：<p><input type="password" name="pwd"></p>
		    <p><input type="submit" value="submit"></p>
		</form>
		
		<!--选中触发onselect-->
		<input type="text" value="12222" class="input1">
		
		<div class="outer">
		    <div class="inner"></div>
		</div>
		
		</body>
		<script src="bom4.js"></script>
		</html>


​		
		//table菜单
		/**
		* Created by Ming on 2017/8/16.
		*/
		var p = document.getElementsByClassName("head")[0];
		p.style.fontSize="40px";
		p.style.textAlign="center";
		
		var d = document.getElementsByClassName("product");
		console.log(d);
		for(var i=0;i<d.length;i++) {
		    d[i].onmouseover = function () {
		        // console.log(this);
		        //获取product标签的内容 txt：iphone
		        var txt = this.innerText;
		        //通过获取class等于txt的a标签
		        var class_p = document.getElementsByClassName(txt)[0];
		        //console.log(class_p);
		        //console.log(class_p.parentElement);
		        //获取class为txt的a 标签的父节点：img-phone。
		        var img_bro = class_p.parentElement;
		        var xianshi = img_bro.className;
		        // img_parent.style.display="inline-block";
		        //获取class为txt的a 标签的父节点的父节点：img。
		        var img_par = img_bro.parentElement;
		        // console.log(img_par);
		        // console.log(img_par.children);
		        //获取父节点img的所有子节点：img-phone,img-ipad。
		        var img_chi = img_par.children;
		        for (var i=0;i<img_chi.length;i++){
		            // console.log(img_chi[i].className=="img-phone");
		            if(img_chi[i].className != xianshi){
		                console.log(img_chi[i]);
		                img_chi[i].style.display="none";
		            }
		            else {
		                console.log(img_chi[i]);
		                img_chi[i].style.display="inline-block";
		            }
		        }
		
		    }
		}
		
		function txt_move() {
		    var head = document.getElementsByClassName("head")[0];
		    var txt = head.innerText;
		    var txt01 =txt.charAt(0);
		    var txt02 = txt.substring(1,txt.length);
		    head.innerText=txt02+txt01;
		}
		setInterval(txt_move, 1000);




		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <title>Title</title>
		    <style>
		        *{
		            margin: 0px;
		        }
		        a{
		            text-decoration-line: none;
		        }
		        .product{
		            display: inline-block;
		            height: 40px;
		            width: 100px;
		            background-color: #f2f2f2;
		            text-align: center;
		            line-height: 40px;
		        }
		        .item{
		            position: absolute;
		            top:5%;
		            left:50%;
		            margin-left: -150px;
		        }
		        .shoplist{
		            width:100%;
		            height: 400px;
		            /*background-color: #42dae0;*/
		            position: relative;
		        }
		        .img1-1{
		            background: url("https://images.apple.com/cn/iphone/compare/images/compare/compare_iphone7_plus_jetblack_medium.jpg") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .img1-2{
		            background: url("https://images.apple.com/cn/iphone/compare/images/compare/compare_iphone6s_plus_spacegray_medium.jpg") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .img1-3{
		            background: url("https://images.apple.com/cn/iphone/compare/images/compare/compare_iphone6s_spacegray_medium.jpg") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .img2-1 {
		            background: url("https://images.apple.com/v/ipad/compare/g/images/compare/compare_ipadpro_silver_medium.png") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .img2-2 {
		            background: url("https://images.apple.com/v/ipad/compare/g/images/compare/compare_ipadpro_10_silver_medium.png") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .img2-3 {
		            background: url("https://images.apple.com/v/ipad/compare/g/images/compare/compare_mini4_silver_medium.png") no-repeat 0 0;
		            display: inline-block;
		            height: 204px;
		            width: 102px;
		        }
		        .imgd1{
		            display: inline-block;
		            padding-left: 50px;
		        }
		        .img-phone{
		            display: inline-block ;
		        }
		        .img-ipad{
		            display: none;
		        }
		        .imgd2{
		            display: inline-block;
		            padding-left: 50px;
		        }
		        span{
		            display: block;
		            text-align: center;
		        }
		        .img{
		            position: absolute;
		            top: 20%;
		            left: 50%;
		            margin-left: -254px;
		        }
		        /*.active{*/
		            /*background-color: #adadad;*/
		        /*}*/
		        .product:hover{
		            background-color:#adadad ;
		        }
		    </style>
		</head>
		<body>
		<div>
		    <div>
		        <p class="head">欢迎光临</p>
		    </div>
		
		    <div class="shoplist">
		        <div class="item">
		            <a href="#" class="product active">iphone</a>
		            <a href="#" class="product">ipad</a>
		            <a href="#" class="product">mac</a>
		        </div>
		        <div class="img">
		            <div class="img-phone">
		                <div class="imgd1 iphone">
		                <a href="" class="img1-1"></a>
		                <span>IPHONE 7 PLUS</span>
		                <span>￥7999.00</span>
		            </div>
		                <div class="imgd1 iphone">
		                <a href="" class="img1-2"></a>
		                <span>IPHONE 6 PLUS</span>
		                <span>￥5999.00</span>
		            </div>
		                <div class="imgd1 iphone">
		                <a href="" class="img1-3"></a>
		                <span>IPHONE 6</span>
		                <span>￥4999.00</span>
		            </div>
		            </div>
		            <div class="img-ipad">
		                <div class="imgd2 ipad">
		                <a href="" class="img2-1"></a>
		                <span>12.9 英寸 iPad Pro</span>
		                <span>￥7999.00</span>
		            </div>
		                <div class="imgd2 ipad">
		                <a href="" class="img2-2"></a>
		                <span>10.5 英寸 iPad Pro</span>
		                <span>￥5999.00</span>
		            </div>
		                <div class="imgd2 ipad">
		                <a href="" class="img2-3"></a>
		                <span>iPad mini 4</span>
		                <span>￥4999.00</span>
		            </div>
		            </div>
		
		        </div>
		    </div>
		
		</div>
		</body>
		<script src="tab.js"></script>
		</html>

onclick 单击

ondbclick 双击

onfocus 获取焦点


onblur 失去焦点

onchange 内容被改变  // select - option 标签

onload 图片、页面加载完成  window.onload=func(){}等窗口读取完之后



onkeydown  按下   场景：回车

onkeypress  按下后松开

onkeyup    松开


onmouserdown 鼠标按钮按下

onmousemove 鼠标移动

onmouseout 离开子标签

onmouseover 悬浮

onmouserleave 从元素离开父标签


onselect 文本选中

onsubmit 确认提交  

onkeydown

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .div1{
	            width:200px;
	            height:200px;
	            background-color: #50ff70;
	        }
	        input{
	            display: inline-block;
	        }
	        .div2{
	            width:200px;
	            height:200px;
	            background-color: #5060ff;
	        }
	    </style>
	</head>
	<body>
	
	<input type="text" id="d1" >
	
	<div class="div1"></div>
	<div class="div2"></div>
	
	</body>
	<script>
	    var ele = document.getElementById("d1");
	//    ele.onkeydown = function (e) {
	    ele.onkeyup = function (e) {
	        alert(e.key);
	
	//        var k = e.keyCode;
	//        var alph = String.fromCharCode(k);
	    }
	
	    var eleM = document.getElementsByClassName("div1")[0];
	    //悬浮
	    //eleM.onmouseover = function () {
	    //按下鼠标
	    eleM.onmousedown = function () {
	        this.style.backgroundColor="#ff6d41";
	
	        //变成小手指标
	        this.style.cursor = 'pointer';
	    }
	    //离开
	    eleM.onmouseout = function () {
	        this.style.backgroundColor="#50ff70";
	    }
	
	</script>
	</html>
	
	onmouseleave and onmouseover
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .container{
	            width: 300px;
	            text-align: center;
	            background-color: #ff6d41;
	        }
	        .list{
	            line-height: 30px;
	        }
	        .item1{
	            background-color: #a143a2;
	        }
	        .item2{
	            background-color: #62ff80;
	        }
	        .item3{
	            background-color: #5060ff;
	        }
	        .title{
	            line-height: 30px;
	        }
	        .list{
	            display: none;
	        }
	    </style>
	</head>
	<body>
	    <div class="container">
	        <div class="title">onmouseout</div>
	        <div class="list">
	            <div class="item1">aaaa</div>
	            <div class="item2">bbbb</div>
	            <div class="item3">cccc</div>
	        </div>
	    </div>
	</body>
	<script>
	    var container = document.getElementsByClassName("container")[0];
	    var title = document.getElementsByClassName("title")[0];
	    var list  = document.getElementsByClassName("list")[0];
	    //悬浮标题显示菜单
	    title.onmouseover = function () {
	        list.style.display="block";
	    };
	    //退出子标签收回菜单
	//    list.onmouseleave = function () {
	//        list.style.display="none";
	//    }
	    //onmouseout 给元素及其子元素绑定
	    container.onmouseleave = function () {
	        list.style.display="none";
	    }
	
	</script>
	</html>

10、作用域与词法分析

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	
	</body>
	<script>
	//    var x = 5, y=10;
	//    function foo() {
	//        var x=9;
	//        function bar() {
	//            //先检查语法
	//            //通过active object 活动对象实现
	//            //1、参数
	//            //2、局部变量声明
	//            //3、函数声明表达式
	//            console.log(x);  //x = 9，如果没有就undefined  --python 就会报错
	//
	//            // 在声明前使用了
	//            var x = 2;
	//            console.log(x); //x = 2
	//        }
	//        bar()
	//    }
	//    foo()
	
	    function f(x,y) {
	        /* 词法分析
	        * AO, x,y = undefined
	        * x = 5; 已经声明
	        * var x = 6;不执行
	        *执行
	        * var x = 6;
	        * 打印x = 6 y = undefined
	        */
	        var x = 6;
	        console.log(x);
	        console.log(y);
	    }
	    f(5);
	</script>
	</html>
	
	11、table
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	
	    </style>
	</head>
	<body>
	<button class="all bt">全选</button>
	<button class="reverse bt">反选</button>
	<button class="cancel bt">取消</button>
	<hr>
	<table border="2px" class="table">
	    <tr>
	        <td><input type="checkbox" class="ite"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	    <tr>
	        <td><input type="checkbox" class="ite"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	    <tr>
	        <td><input type="checkbox" class="ite"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	
	</table>
	</body>
	<script>
	//    var ele_all = document.getElementsByClassName("all")[0];
	//    var ele_reverse = document.getElementsByClassName("reverse")[0];
	//    var ele_cancel = document.getElementsByClassName("cancel")[0];
	//    ele_all.onclick = function () {
	//        var ite = document.getElementsByClassName("ite");
	//        for (var i=0;i<ite.length;i++ ){
	//            ite[i].checked=true;
	//        }
	//    };
	//    ele_reverse.onclick = function () {
	//        var ite = document.getElementsByClassName("ite");
	//        for (var i=0;i<ite.length;i++ ){
	//            if (ite[i].checked==true){
	//                ite[i].checked=false;
	//            }
	//            else{
	//                ite[i].checked=true;
	//            }
	//        }
	//    ele_cancel.onclick = function () {
	//        var ite = document.getElementsByClassName("ite");
	//        for (var i=0;i<ite.length;i++ ){
	//            ite[i].checked=false;
	//        }
	//    };
	//    }
	
	//优化版本
	    var bt = document.getElementsByClassName("bt");
	    var box = document.getElementsByClassName("ite");
	    for (var i=0;i<bt.length;i++) {
	        bt[i].onclick = function () {
	            console.log(this.innerText);
	            if (this.innerText == "全选") {
	                for (var i=0;i<box.length;i++){
	                    box[i].checked=true;
	                }
	            }
	            else if (this.innerText == "反选") {
	
	                for (var i=0;i<box.length;i++){
	                    if(box[i].checked==true){
	                        box[i].checked=false;
	                    }
	                    else
	                    {
	                        box[i].checked=true;
	                    }
	                }
	            }
	            else if (this.innerText == "取消") {
	                for (var i=0;i<box.length;i++){
	                    box[i].checked=false;
	                }
	            }
	        }
	
	    }
	
	</script>
	</html>


12、select移动

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	    #left{
	        width: 200px;
	        height: 70px;
	        background-color: #a2768f;
	    }
	    #right{
	        width: 200px;
	        height: 70px;
	        background-color: #3c96a2;
	    }
	    span{
	        display: inline-block;
	        background-color: #e0e0e0;
	        text-align: center;
	        width: 100px;
	        height: 100px;
	        line-height: 30px;
	        vertical-align: top;
	        /*基线对齐*/
	    }
	    select{
	
	    }
	    </style>
	</head>
	<body>
	<select name="" id="left" size="3" multiple="multiple">
	    <option value="ch" class="op">语文</option>
	    <option value="ma" class="op">数学</option>
	    <option value="en" class="op">英语</option>
	</select>
	<span>
	    <button class="torb"> >  </button>
	    <br>
	    <button class="torba"> >>>  </button>
	    <br>
	    <button class="tolb"> <  </button>
	</span>
	<select name="" id="right" size="3"  multiple="multiple">
	  <option value="ch" class="op">化学</option>
	</select>
	</body>
	<script>
	    var torb = document.getElementsByClassName("torb")[0];
	    var torba = document.getElementsByClassName("torba")[0];
	    var tolb = document.getElementsByClassName("tolb")[0];
	    var option_arr_left = document.getElementById("left");
	    var option_arr_right = document.getElementById("right");
	
	    torb.onclick = function () {
	        for (var i = 0; i < option_arr_left.length; i++) {
	            console.log(i);
	            if (option_arr_left[i].selected) {
	                option_arr_right.appendChild(option_arr_left[i]);
	                i--;
	            }
	        }
	    }
	  torba.onclick = function () {
	        for (var i = 0; i < option_arr_left.length; i++) {
	            option_arr_right.appendChild(option_arr_left[i]);
	            i--;
	        }
	    }
	    tolb.onclick = function () {
	        for (var i = 0; i < option_arr_right.length; i++) {
	            if (option_arr_right[i].selected) {
	                option_arr_left.appendChild(option_arr_right[i]);
	                i--;
	            }
	        }
	    }
	
	</script>
	
	</html>

​	
















