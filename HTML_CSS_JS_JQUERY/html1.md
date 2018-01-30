# 一、http协议（hypertext transport protocol超文本传输协议）

服务器与浏览器通信的规则，是一个无状态的协议，每次请求无关。

URL：协议名：//域名.端口/路径（80）

DNS：域名解析，解析成ip地址

	浏览器发送一次请求就是标准的CS模式
	请求协议--》浏览器给服务器
	
	1、请求首行： GET：请求方式   / HTTP/1.1：http版本
	2、请求头信息：发送请求的详细解释
	Host: 127.0.0.1:8080
	Connection: keep-alive   连接一小段时间后断开
	Cache-Control: max-age=0
	Upgrade-Insecure-Requests: 1
	User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
	Accept-Encoding: gzip, deflate, br
	Accept-Language: zh-CN,zh;q=0.8
	3、—---空行----
	4、请求体（包含请求数据）GET没有，只有POST有
	GET：
	     特点：
	     （1）发送请求的方式https://leetcode.com/?a=1  a=1就是参数，参数在地址栏中，安全性低。
	     （2）数据在1K之内
	     
	     操作：
	     （1）地址栏输入网址
	     （2）点击超链接
	     （3）提交表单，默认使用GET，但是一般用POST
	
	POST：
	     特点：
	     （1）不在地址栏
	     （2）大小没有上限
	     （3）有请求体
	     （4）请求体如果使用中文，会使用URL编码
	
	
	从百度搜素“IT培训”进入51cto
		- :authority:static1.51cto.com
		- :method:GET
		- :path:/edu/center/images/index/nav_icon.png
		- :scheme:https
		- accept:image/webp,image/apng,image/*,*/*;q=0.8
		- accept-encoding:gzip, deflate, br
		- accept-language:zh-CN,zh;q=0.8
		- cookie:www51cto=F8F34ECA4ADC2938EC51914928ACAC38CQsG; Hm_lvt_110fc9b2e1cae4d110b7959ee4f27e3b=1495165592; looyu_id=066e1e2c3ff7dbe2f5886d8c4f64641836_20000923%3A4; pub_smile=1DD0D9
		- referer:https://static1.51cto.com/edu/center/css/home.css?v=1.0.5 通过其他连接进入，可以用于统计，或查看盗链
		- user-agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36
		- Cookie: sessionid=xxxxxxxxxxxxxx 关键字保存状态：记录用户操作，返回给浏览器页面的时候同时返回cookie，下次连接由浏览器发送请求协议和数据及cookie给服务器。
	



	响应协议--》服务器给浏览器
	（1）响应首行
	Request URL:
	https://www.baidu.com/
	Request Method:
	GET
	Status Code:
	200 OK  状态码 302:重定向  304：用户一次发送请求之后，服务器会添加Last-modified响应头，说明最后修改时间，浏览器会把网页和最后响应时间保存下载，第二次请求，在请求头包含一个IF-Modified-Since请求头，如果服务器判断两个modified头时间相等就让用户从缓存里读取网页
	Remote Address:
	14.215.177.38:443
	Referrer Policy:
	no-referrer-when-downgrade
	
	
	Bdpagetype:
	Bdqid:
	0xdf6d056e00001cb9
	Bduserid:
	2245351645
	Cache-Control:
	private
	Connection:
	Keep-Alive
	Content-Encoding:
	gzip
	Content-Type:
	text/html;charset=utf-8 #浏览器收到的信息格式
	Date:
	Wed, 09 Aug 2017 02:34:09 GMT
	Expires:
	Wed, 09 Aug 2017 02:34:09 GMT
	Server:
	BWS/1.1  # 服务器软件名称   apache, nginx 
	Set-Cookie:
	BDSVRTM=254; path=/  #设置cookie
	Set-Cookie:
	BD_HOME=1; path=/
	Set-Cookie:
	H_PS_PSSID=1436_21088_20718; path=/; domain=.baidu.com
	Strict-Transport-Security:
	max-age=172800
	Transfer-Encoding:
	chunked
	X-Ua-Compatible:
	IE=Edge,chrome=1
	Accept:
	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
	Accept-Encoding:
	gzip, deflate, br
	Accept-Language:
	zh-CN,zh;q=0.8
	Cache-Control:
	max-age=0
	Connection:
	keep-alive
	Cookie:
	BAIDUID=940575BC3DD667C7412C4EA9398BC50E:FG=1; BIDUPSID=940575BC3DD667C7412C4EA9398BC50E; PSTM=1498819460; MCITY=-257%3A; ispeed_lsm=2; sugstore=0; BDUSS=B3bjZkMWNYVDlkWndCcWlMMjBTcjZiMUFnMGxnbVI2dkNPOXVOMjZMbVJTYWxaSVFBQUFBJCQAAAAAAAAAAAEAAADdWNWFTWF0dExldW45AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJG8gVmRvIFZMX; BD_HOME=1; H_PS_PSSID=1436_21088_20718; BD_UPN=12314353
	Host:
	www.baidu.com
	Upgrade-Insecure-Requests:
	User-Agent:
	Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36



二、html超文本标记语言

	<!DOCTYPE html>  告知浏览器文档使用哪种规范 html/xhtml
	<html lang="en"> 
	    <head>
	        <meta charset="UTF-8"> #编解码
	        <meta name="keywords" content="IT培训">  #搜索使用到的关键词
	        <meta name="decription" content="IT培训"> #描述信息
	        <meta http-equiv="refresh" content="3;www.baidu.com"> #设置响应头，3秒跳转
	        <meta http-equiv="content-type" charset="utf8"> #返回给浏览器的数据的解码格式
	        <title>lalalal</title>
	        <link rel="icon" href="//www.jd.com/favicon.ico"># 设置浏览器左上方图标
	  #设置背景颜色
	  <style>
	        h1{
	            background: red;
	            font-size: 30px;
	        }
	        p{
	            background: gold;
	        }
	        sub{
	            background: green;
	        }
	        div{
	            background: greenyellow;
	                  height: 300px;
	         }
	  #mao1{
	      background: hotpink;
	  }
	  #mao2{
	      background: lightskyblue;
	  }
	  #mao3{
	      background: yellow;
	  }
	
	        span{
	            background: aqua;
	        }
	
	    </style>
	</head>
	<body>
	<!--标题 独占一行-->
	<h1>lalala</h1>
	<h2>lalala</h2>
	<h3>lalala</h3>
	<h4>lalala</h4>
	<h5>lalala</h5>
	
	<!--文本段落 独占一行-->
	<p>abcde</p>
	<p>fghij</p>
	<p>klmno</p>
	
	<!--加粗-->
	<b>abcde</b>
	<strong>abcde</strong>
	
	<!--横线-->
	<strike>100</strike>
	
	<!--斜体-->
	<em>100</em>
	
	<!--下标-->
	2<sub>3</sub>
	2<sup>3</sup>
	
	<!--换行-->
	<br>
	
	<!--分割线-->
	<hr>
	
	<!--用于CSS-->
	<div>lalala</div>
	<span>lalala</span>
	
	<!--插入图片 title：鼠标放上去显示的信息 alt:显示失败后显示的信息-->
	<img src="http://lh6.ggpht.com/VxzVq8v0fMjdh_Ue5cvFtZ5AuT1b5IhaQFgzBe9V1rUce20Rwyt5VfTkEEVKlmOBOdqR24UwMk1SH5rBzTKpdn4UJkg6HFIshUb2fogXXQ=s0" alt="" width="200px" title="star">
	         
	<!--超链接-->
	<a href="\untitled\day10\index.html"><img src="http://lh6.ggpht.com/VxzVq8v0fMjdh_Ue5cvFtZ5AuT1b5IhaQFgzBe9V1rUce20Rwyt5VfTkEEVKlmOBOdqR24UwMk1SH5rBzTKpdn4UJkg6HFIshUb2fogXXQ=s0" alt="star" title="start"></a>
	
	<!--锚-->
	<div id="mao1">锚1</div>
	<div id="mao2">锚2</div>
	<div id="mao3">锚3</div>
	<div id="mao4">锚4</div>
	<div id="mao5">锚5</div>
	<a href="#mao1">===返回锚1===</a>
	<a href="#mao2">===返回锚2===</a>
	
	<!--列表：无序列表、有序列表、定义列表-->
	<!--无序-->
	<ul>
	    <li>111</li>
	    <li>222</li>
	    <li>333</li>
	</ul>
	
	<!--有序-->
	<ol>
	    <li>111</li>
	    <li>222</li>
	    <li>333</li>
	</ol>
	
	<!--定义-->
	<dl>
	    <dt>标题</dt>
	    <dd>222</dd>
	    <dd>333</dd>
	</dl>
	<!--表格-->
	<!--border边框宽度 cellspacing内边框宽度 cellpadding外边框宽度  -->
	<table border="2px" cellspacing="0px" cellpadding="3px" >
	    <tr>
	        <td>标题</td>
	        <td>标题</td>
	    </tr>
	    <tr>
	        <!--占两行，用于合并单元格-->
	        <td rowspan="2">内容</td>
	        <td>内容</td>
	    </tr>
	    <tr>
	
	        <td>内容</td>
	    </tr>
	    <tr>
	        <!--占两列，用于合并单元格-->
	        <td colspan="2">内容</td>
	    </tr>
	</table>
	 
	    </body>
	</html>

1、标签分类

1.1 块级标签 --block :独占一行 h 、p 、div

1.2 内联标签 --inline

：根据文件内容而定 sub、sup 、span

1.3 url 统一资源定位符

第一部分：协议http:// ftp://

第二部分：站点地址 域名或者ip

第三部分：站点目录、文件

1.4 表单

用于向服务器传输数据，从而实现用户与web服务器的交互

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>From</title>
	</head>
	<body>
	<h1>注册</h1>
	<form action="" method="post">
	    <p>用户名：<input type="text" name="username"></p>
	    <p>密码：<input type="password" name="password"></p>
	
	    <!--input 重点 checked="checked" 默认选择-->
	    <p>爱好：1<input type="checkbox" name="h" value="1" checked="checked">
	            2<input type="checkbox" name="h" value="2">
	            3<input type="checkbox" name="h" value="3"></p>
	
	              <!--type="radio" 互斥>
	    <p>性别: 男<input type="radio" value="男" name="gender" value="male">
	            女<input type="radio" value="女" name="gender" value="female">
	            保密<input type="radio" value="保密" name="gender"  value="anonymous"></p>
	
	
	    <!--下拉框 重点  size="X":默认显示个数  multiple="multiple"：多选-->
	    <p>国家: <select name="country" id="" size="3" multiple="multiple">
	            <!--分组-->
	            <optgroup label="世界各国">
	            <!--selected="selected" 默认 -->
	            <option value="中国" selected="selected">中国</option>
	            <option value="美国">美国</option>
	            <option value="日本">日本</option>
	            </optgroup>
	
	        </select>
	    </p>
	
	    <!--文本框 内联-->
	    <p>简介：</p>
	    <p><textarea name="te" id="1" cols="30" rows="10" ></textarea></p>
	
	    <!--label标签 动态指引 ：点击文字自动切换到文本框输入-->
	    <label for="username">用户名</label>
	    <input type="text" name="username" id="username">
	
	    <!--外加一个框  少用-->
	    <fieldset>
	        <legend>登录框</legend>
	        <input type="text">
	    </fieldset>
	
	    <p><input type="submit" value="submit"></p>
	    <p><input type="button" value="button"></p>
	    <p><input type="hidden"></p>
	    <p><input type="file" name="filename"></p>
	
	</form>
	</body>
	</html>

三、CSS
1、查到标签（选择器）
1.1基本选择器

	1. 标签选择器  p{color : red; }
	2. id 选择器    #info{color : red; }
	3. class选择器 .info{color : red; }
	4. 通配选择器  * {color : red; }
	5. 组合选择器 


	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>CSS</title>
	    <!--css第二种引入方式-->
	    <!--<style>-->
	    <!--p{-->
	        <!--background-color: gold;-->
	    <!--}-->
	    <!--</style>-->
	
	    <!--css第三种引入方式-->
	    <link rel="stylesheet" href="\untitled\day10\1\css_test.css">
	
	    <!--css第四种引入方式-->
	    <!--<style>-->
	        <!--@import "css_test.css";-->
	    <!--</style>-->
	
	</head>
	<body>
	
	<!--css第一种引入方式  不常用-->
	<!--<p style="background: red;color: aqua">Hello</p>-->
	
	<!--#p1{-->
	    <!--background-color: aqua;-->
	<!--}-->
	<!--#p2{-->
	    <!--background-color: darkviolet;-->
	<!--}-->
	<p id="p1">hello</p>
	<p id="p2">hello</p>
	
	<!--常用：对局部标签进行渲染-->
	<!--p.c{-->
	        <!--background-color: darkolivegreen;-->
	<!--}-->
	<p class="c">hello</p>
	<p class="c">hello</p>
	<p>hello</p>
	
	<!--.page{-->
	    <!--display: inline-block;-->
	    <!--width: 20px;-->
	    <!--height:20px;-->
	    <!--background-color: aquamarine;-->
	    <!--color: darkblue;-->
	<!--}-->
	<!--#first_index{-->
	    <!--background-color: chartreuse;-->
	<!--}-->
	<ul>
	    <li id='first_index' class="page">1</li>
	    <li class="page">2</li>
	    <li class="page">3</li>
	    <li class="page">4</li>
	    <li class="page">5</li>
	</ul>
	
	<!--要求1：让outer的p全部变红（后代重点）-->
	<!--.outer p{-->
	    <!--color: red;-->
	<!--}-->
	
	<!--要求2：让outer的子代p全部变白-->
	<!--.outer>p{-->
	    <!--color: white;-->
	<!--}-->
	
	<!--要求3：让outer的向下毗邻p全部变白-->
	<!--.outer+p{-->
	    <!--color: white;-->
	<!--}-->
	
	<!--要求4：让outer的向下的兄弟p全部变红白-->
	<!--.outer~p{-->
	    <!--color: red;-->
	<!--}-->
	
	<div class="outer">
	    <div class="inner">
	        <p>后代
	            <p>后代</p>
	        </p>
	    </div>
	    <p>子代</p>
	</div>
	
	<!--/*同时设置*/-->
	<!--.p1, .div1{-->
	    <!--color: red;-->
	<!--}-->
	<p class="p1">毗邻</p>
	<div class="div1">div</div>
	<p>不毗邻</p>
	</body>
	</html>



2、操作标签（属性操作）

1.1 行内式

1.2 嵌入式

1.3 链接式 （推荐）

1.4 导入时（了解）

3、继承与优先级

3.1 父类所设置都被子类继承

3.2 sytle 1000 > #id级别 100 >.类级别 10> 标签级别 1

同级别按照顺序（更近的）

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .c1[po]{
	            color: red;
	        }
	        /*类似正则 *=:只要含有 $=结尾是 ~=具有多个空格，其中一个值等于  ^=以开头 */
	        .c1[po*="p2"]{
	            color: yellowgreen;
	        }
	        .c1[po~='p']{
	            font-size: 30px;
	        }
	        .c1{
	            color: red;
	        }
	        #d1{
	            color: yellowgreen;
	        }
	        .c1 p{
	
	            color: darkblue;
	        }
	        /*!import 最高优先级*/
	        .p3{
	            color: gold!important;
	        }
	
	    </style>
	</head>
	<body>
	
	<div id="d1" po="p2" class="c1">lalala</div>
	<div po="eqwp2eqw" class="c1">lalala</div>
	<div class="c1">lalala
	    <p class="p3">laldawdawala</p>
	</div>
	
	</body>
	</html>

4、css test、背景图片

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        p{
	            /*color: RGB(100,125,120);*/
	            /*A 是透明度 0.0~1.0*/
	            color: RGBA(255,0,0,0.5);
	            /*十六进制*/
	            /*color: #ff2d85;*/
	            font-size: 50px;
	            /*opacity也是透明度*/
	            opacity: 1;
	        }
	        div{
	            width: 800px;
	            height: 800px;
	            background-color: yellowgreen;
	            /*文字水平对齐 center right */
	            text-align:center ;
	            /*背景图片*/
	            /*background-image: url("https://media-cdn.tripadvisor.com/media/photo-s/0a/7b/7b/c6/restaurant-view.jpg");*/
	            /*背景图片平铺方式*/
	            /*background-repeat: no-repeat;*/
	            /*背景图片位置*/
	            /*background-position:center center;*/
	            /*background-position:150px 150px;*/
	
	            /*简单写法*/
	            background: url("https://media-cdn.tripadvisor.com/media/photo-s/0a/7b/7b/c6/restaurant-view.jpg") no-repeat center center;
	        }
	        /*justify 两端对齐*/
	        div .p1{
	            text-align:justify ;
	        }
	    </style>
	</head>
	<body>
	<div>div
	    <p class="p1">qqqqqqqqq</p>
	
	</div>
	<p>hello</p>
	</body>
	</html>

5、border

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        div{
	            width: 500px;
	            height: 500px;
	            background-color: aqua;
	            /*简写 border:3px solid red;*/
	            border-width: 5px;
	            border-style:dashed;
	            border-color: fuchsia;
	        }
	    </style>
	</head>
	<body>
	<div>
	    div
	</div>
	</body>
	</html>

6、list-style

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        ul {
	            list-style-type: none;
	            /*list-style-image: url("http://dig.chouti.com/images/logo.png");*/
	        }
	    </style>
	</head>
	<body>
	<!--ul>li.item*3-->
	<ul>
	    <li class="item">111</li>
	    <li class="item">222</li>
	    <li class="item">333</li>
	</ul>
	</body>
	</html>

7、display

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        /*移动鼠标至c1 c2消失*/
	        div{
	            width:200px;
	            height: 200px;
	            background-color: saddlebrown;
	        }
	        .c2{
	            width:100px;
	            height: 100px;
	            background-color: darkmagenta;
	        }
	        .c1:hover .c2{
	            /*隐藏没有物理空间*/
	            /*display: none;*/
	
	            /*隐藏有物理空间*/
	            visibility: hidden;
	        }
	        .c3{
	            width:100px;
	            height: 100px;
	            background-color: silver;
	        }
	        .c4{
	            width:100px;
	            height: 100px;
	            background-color: yellowgreen;
	
	        }
	        span{
	            width:50px;
	            height: 50px;
	            background-color: wheat;
	          /*既有内联并列排列和块的设置长宽属性 或者相互变换*/
	            display: inline-block;
	        }
	
	    </style>
	</head>
	<body>
	
	<div class="c1">hello
	<div class="c2">c2</div>
	<div class="c3">c3</div>
	<div class="c4">c4</div>
	</div>
	<span>qweqwe</span>
	<a href="">weqewqeqw</a>
	
	</body>
	</html>

8、伪类

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        a:link{
	            color: brown;}
	        /*悬浮*/
	        a:hover{
	            color: aquamarine;}
	        /*点击之后*/
	        a:visited{color: fuchsia}
	        /*按下去瞬间*/
	        a:active{
	            color: chartreuse;}
	        .top{
	            background-color: #204982;
	            width: 200px;
	            height: 200px;
	        }
	        .botton{
	            background-color: wheat;
	            width: 200px;
	            height: 200px;
	        }
	        /*.d1:hover .top{*/
	            /*background-color: blue;*/
	        /*}*/
	        .d1:hover .botton{
	            background-color: yellow;
	        }
	        /*伪类*/
	        p:after{
	            content: "world";
	            color: peachpuff;
	        }
	    </style>
	</head>
	<body>
	<!--anchor伪类-->
	<a href="#">hello adsdsadada</a>
	
	<div class="d1">
	    <div class="top"></div>
	    <div class="botton"></div>
	    <div class="clearfix"></div>
	</div>
	<p>hello</p>
	</body>
	</html>


9、margin padding


	<!DOCTYPE html>
	<html lang="en">
	<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        /**{*/
            /*margin: 0px;*/
        /*}*/
        .box{
            width:100px;
            height:100px;
            background-color: rebeccapurple;
            /*元素与元素之间的距离，如果两元素出现冲突，取最大*/
            /*margin: 100px;*/
            /*盒子大小*/
            padding: 0px;
            /*border: solid 5px;*/
        }
        .box1{
            width:300px;
            height:300px;
            background-color: #33997c;
            /*元素与元素之间的距离*/
            margin: 10px;
            /*内容与边框的距离*/
            padding: 20px;
            border: solid 5px;
        }
        .outer{
            overflow: hidden;
            width: 300px;
            height: 300px;
            background-color: aqua;
            padding-left: 200px;
            padding-top: 200px;
        }
    </style>
</head>
<body>
<div class="outer">
    <div class="box"></div>
    <div class="box1"></div>
</div>
</body>
</html>



10、float
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .div1{
            width:300px;
            height: 50px;
            background-color: #a143a2;
        }
        .div2{
            /*左浮动*/
            /*下方div如果不是浮动会与上方元素保持垂直*/
            float: left ;
            width:100px;
            height: 200px;
            background-color: #33a235;
        }
        .div3{
            width:180px;
            height: 150px;
            background-color: #1d3aa2;
        }
    </style>
	</head>
	<body>
	<div class="div1"></div>
	<div class="div2"></div>
	<div class="div3"></div>
	</body>
	</html>
	
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .div1{
            width:300px;
            height: 50px;
            background-color: #a143a2;
            float: right;
        }
        .div2{
            /*左浮动*/
            /*下方div如果不是浮动,是就紧贴，不是会与上方元素保持垂直*/
            float: right ;
            width:100px;
            height: 200px;
            background-color: #33a235;
        }
        .div3{
            float: right;
            width:180px;
            height: 150px;
            background-color: #1d3aa2;
        }
    </style>
	</head>
	<body>
	<div class="div1"></div>
	<div class="div2"></div>
	<div class="div3"></div>
	</body>
	</html>
	
	
	清除浮动clear：left 清除上一个元素的左浮动，影响的是自己
	<!DOCTYPE html>
	<html lang="en">
	<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .div1{
            width:300px;
            height: 50px;
            background-color: #a143a2;
            float: left;

        }
        .div2{
            /*左浮动*/
            /*哪里浮动往哪里贴，没有浮动就垂直*/
            float: left ;
            width:100px;
            height: 200px;
            background-color: #33a235;
            clear: left;
        }
        .div3{
            float: left;
            width:180px;
            height: 150px;
            background-color: #1d3aa2;
        }
    </style>
	</head>
	<body>
	<div class="div1"></div>
	<div class="div2"></div>
	<div class="div3"></div>
	</body>
	</html>

绿色清除浮动前：

绿色清除浮动后：

11、塌陷

	<!DOCTYPE html>
	<html lang="en">
	<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        .box1{
            width:300px;
            height: 300px;
            background-color: #a143a2;
            float: left;
        }
        .box2{
            width:300px;
            height: 300px;
            background-color: #1600a2;
            float: left;
        }
        .foo{
            width:100%;
            height: 50px;
            background-color: #a20f04;

        }
        /*.container{*/
            /*!*解决父级塌陷*!*/
            /*overflow:hidden;*/
        /*}*/
        /*伪类增加一行空内容也可以解决*/
        .clearfix:after{
            content: '';
            display: block;
            clear: both;
        }
    </style>
	</head>
	<body>
	<div class="container clearfix">
    <div class="box1">box1</div>
    <div class="box2">box2</div>

	</div>
	<div class="foo">footer</div>
	</body>
	</html>
	box1、box2的父级container是空的，造成父级塌陷
	上述情况，outer为空设置box的margin，会自动找父级的margin,父级没有最后找到body的magin，设置body的margin
	需要在outer设置overflow: hidden;就能解决

12、position

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .box1{
	            width:300px;
	            height: 300px;
	            background-color: #a143a2;
	
	        }
	        .box2{
	            width:300px;
	            height: 300px;
	            background-color: #1600a2;
	            /*相对定位 自己当前位置*/
	            /*position: relative;*/
	            /*绝对定位 父级版面位置*/
	            position: absolute;
	            top: 100px;
	            left: 100px;
	        }
	        .foo{
	            width:100%;
	            height: 50px;
	            background-color: #a20f04;
	
	        }
	
	    </style>
	</head>
	<body>
	<div class="container clearfix">
	    <div class="box1">box1</div>
	    <div class="box2">box2</div>
	</div>
	<div class="foo">footer</div>
	</body>
	</html>
	定位技巧：父级设置为relative 自己设置为absolute
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        *{
	            margin: 0px;
	        }
	        .box1{
	            width:300px;
	            height: 300px;
	            background-color: #a143a2;
	
	        }
	        .box2{
	            width:300px;
	            height: 300px;
	            background-color: #1600a2;
	            /*相对定位 自己当前位置*/
	            /*position: relative;*/
	            /*绝对定位 父级版面位置*/
	            position: absolute;
	            top: 300px;
	            left: 300px;
	        }
	        .foo{
	            width:100%;
	            height: 50px;
	            background-color: #a20f04;
	
	        }
	        .container{
	            border: 2px solid rebeccapurple;
	            position: relative;
	        }
	    </style>
	</head>
	<body>
	<div class="container clearfix">
	    <div class="box1">box1</div>
	    <div class="box2">box2</div>
	</div>
	<div class="foo">footer</div>
	</body>
	</html>
	
	
	/*绝对定位 广告框*/
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        *{
	            margin: 0px;
	        }
	        .box1{
	            width:300px;
	            height: 300px;
	            background-color: #a143a2;
	
	        }
	        .box2{
	            width:1300px;
	            height: 1300px;
	            background-color: #1600a2;
	            /*相对定位 自己当前位置*/
	            /*position: relative;*/
	            /*绝对定位 父级版面位置*/
	            position: absolute;
	            top: 300px;
	            left: 300px;
	        }
	        .foo{
	            width:100%;
	            height: 50px;
	            background-color: #a20f04;
	            /*绝对定位 广告框*/
	        }
	        .container{
	            border: 2px solid rebeccapurple;
	            position: relative;
	        }
	        .returntop{
	            width:80px;
	            height:80px;
	            background: red;
	            position: fixed;
	            text-align: center;
	            line-height: 80px;
	            bottom: 20px;
	            right: 10px;
	        }
	    </style>
	</head>
	<body>
	<div class="container clearfix">
	    <div class="box1">box1</div>
	    <div class="box2">box2</div>
	</div>
	<div class="foo">footer</div>
	<div class="returntop">return top</div>
	</body>
	</html>


13、脱离文档流：float position fixed

14、抽屉网页页面布局



