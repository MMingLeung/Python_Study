一、JQUERY是什么？
封装了JS很多函数的库，提供很多简洁的方法

二、JQUERY对象
"$" == Jquery 

三、选择器
	
	基本选择器：
	//    $("*").css("color", "blue")
	//    $("#p2").css("color", "yellow")
	//    $(".p3").css("color", "#ffffff")
	//      $(".p3,#p2").css("color","red")
	
	基本筛选器：
	
	//筛选器
	//  $("ul .item").css("color","red");
	//  $("li:first").css("color","white");
	//    $("li:last").css("color","white");
	
	//    $("ul li:eq(4)").css("color","white");//指定任意一个标签
	//    $("ul li").eq(4).css("color","red");//推荐
	//    var $ret = $("ul li").eq(3).hasClass("item");//如果class有item返回T ，否则F
	//    $("ul li:even").css("color","white");
	//    $("ul li:odd").css("color","white");
	
	    //找到3后面所有列表标签
	    //大于
	//    $("ul li:gt(3)").css("color","white");
	    //小于
	//    $("ul li:lt(3)").css("color","white");
	
	//属性筛选器
	//    $("[lalala]").css("color","red")
	//    $("[lalala=baba]").css("color","red")
	
	// 表单筛选器
	//    $(":text").css("width","200px");
	
	//--------查找筛选器--------
	//    子代组
	//.children 找div1标签的<子代>标签的a标签
	//var $chil = $(".div1").children("a");
	//$(".div1").children("p").css("color","red");
	//.find 找<后代>
	//$(".div1").find("p").css("color","red");
	
	//    兄弟组 下一个next 下面全部nextall 下面直到某一个nextuntil
	//$("ul .item1").next("p").css("color","red");
	
	//上一个prev prevall preUntil
	
	//parent parents parentUntil
	
	//其他兄弟sibling
	    $(".item5").siblings().css("color",'red')

四、属性操作

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	
	<div>DIV
	    <a href="#">kakakak</a>
	</div>
	
	<input type="checkbox" name="hobby" value="1">
	<input type="text" value="1">
	<input type="button" value="1">
	
	<p value="qwe">PPP</p>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    //prop方法控制标签属性
	//    $(":checkbox").prop('checked');//取值
	//    $(":checkbox").prop('checked',true);//赋值
	//    $(":checkbox").attr('checked',true);固有属性不用attr，只能操作自定义属性
	
	    //addClass removeClass
	
	    //html() text()
	    //取值
	    $("div").html();
	    $("div").text();
	    //赋值
	    $("div").html("<h1>lala</h1>");
	    $("div").text("<h1>lala</h1>");
	
	//    console.log($("input").val());
	    console.log($(":checkbox").val());
	    console.log($(":button").val());
	
	</script>
	</html>

左侧菜单实现：
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	
	    <style>
	        .menu{
	            height:500px;
	            width: 30%;
	            background-color: #ff6d41;
	            float: left;
	        }
	        .content{
	            height: 500px;
	            width: 70%;
	            background-color: #a143a2;
	            float: left;
	        }
	        .title{
	            line-height: 50px;
	            background-color: #2459a2;
	            color: #62ff80;
	        }
	        .hide{
	            display: none ;
	        }
	    </style>
	</head>
	<body>
	<div class="outer">
	    <div class="menu">
	        <div class="item">
	            <div class="title" onclick="show(this)">菜单一</div>
	            <div class="con">
	            <div>111</div>
	            <div>111</div>
	            <div>111</div>
	            <div>111</div>
	        </div>
	        </div>
	        <div class="item">
	            <div class="title" onclick="show(this)">菜单二</div>
	            <div class="con hide">
	            <div>222</div>
	            <div>222</div>
	            <div>222</div>
	            <div>222</div>
	        </div>
	        </div>
	        <div class="item">
	            <div class="title" onclick="show(this)">菜单三</div>
	            <div class="con hide">
	            <div>333</div>
	            <div>333</div>
	            <div>333</div>
	            <div>333</div>
	        </div>
	        </div>
	    </div>
	    <div class="content">
	
	    </div>
	</div>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	function show(self) {
	    console.log(self.innerText);//是dom 对象
	    console.log($(self).text());//Jquery获取文本内容
	    $(self).next().removeClass("hide");
	
	    // 链式操作
	    $(self).parent().siblings().children(".con").addClass("hide");
	
	}
	
	</script>
	</html>

五、循环
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	<ul>
	    <li>1</li>
	    <li>2</li>
	    <li class="item">3</li>
	    <li>4</li>
	</ul>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	
	    arr = [123,345,678,'lalala'];
	    obj = {"name":'matt',"age":'12'};
	    //$.each(arr,funtion(){})循环
	    $.each(arr,function(i,j){
	        console.log(i,j)
	    });
	    $.each(obj,function(i,j){
	        console.log(i,j)
	    });
	    //
	    $("ul li").each(function(){
	        if ($(this).hasClass("item")){
	            alert($(this).text());
	        }
	    })
	
	</script>
	</html>

正反选择循环实例：

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	<button f="ite" class="all bt" onclick="func1(this)">全选</button>
	<button f="c2" class="reverse bt" onclick="func1(this)">反选</button>
	<button f="c3" class="cancel bt" onclick="func1(this)">取消</button>
	<hr>
	<table border="2px" class="table">
	    <tr>
	        <td><input type="checkbox" class="ite c1"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	    <tr>
	        <td><input type="checkbox" class="ite c2"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	    <tr>
	        <td><input type="checkbox" class="ite c3"></td>
	        <td>2</td>
	        <td>3</td>
	    </tr>
	
	</table>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    function func1(self) {
	            //方式一：
	        if ($(self).text()=="全选") {
	            $(".all").siblings(".table").find(":checkbox").prop("checked", true);
	//            console.log($ele);
	        }
	        else if ($(self).text()=="反选"){
	            //方法一：
	//            var $ele = $(".all").siblings(".table").find(":checkbox");
	//            for(var i=0;i<$ele.length;i++){
	//                console.log($ele[i].checked);
	//                if ($ele[i].checked==false){
	//                    $ele[i].checked=true;
	//              }
	//        else {
	//                    $ele[i].checked=false;
	//                }
	//            }
	            //方法二：使用jquery循环
	            $(":checkbox").each(function () {
	                $(this).prop("checked",!$(this).prop("checked"));
	//                    if($(this).prop("checked")){
	//                        $(this).prop("checked",false);
	//                    }
	//                    else {
	//                        $(this).prop("checked",true);
	//                    }
	            })
	      }
	        else if ($(self).text()=="取消"){
	            $(".all").siblings(".table").find(":checkbox").prop("checked", false);
	        }
	
	    }
	</script>
	</html>

切换实现：
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<style>
	.nav li{
	    float: left;
	    list-style: none;
	    width: 100px;
	    height: 50px;
	    background-color: #62ff80;
	    text-align: center;
	    line-height: 50px;
	    border-right: solid 1px orangered;
	}
	.content{
	    width: 303px;
	    height: 300px;
	    background-color: #e0e0e0;
	    float: left;
	    margin-left: 40px;
	}
	ul .active{
	    background-color: #84a42b;
	}
	.hide{
	    display: none;
	}
	</style>
	<body>
	<div class="outer">
	    <ul class="nav">
	        <li f="c1" class="active ll">菜单一</li>
	        <li f="c2">菜单二</li>
	        <li f="c3">菜单三</li>
	    </ul>
	    <div class="content">
	        <div class="c1">111</div>
	        <div class="c2 hide">222</div>
	        <div class="c3 hide">333</div>
	    </div>
	</div>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    var ele = document.getElementsByClassName("outer")[0];
	    var li = ele.getElementsByTagName("li");
	
	    for(var i=0;i<li.length;i++){
	        li[i].onclick = function () {
	            $(this).addClass("active");
	            $(this).siblings().removeClass("active");
	            //方法一：
	//            if ($(this).text()=="菜单一"){
	//                $(this).parent().next().children(".c1").removeClass("hide").siblings().addClass("hide");
	//            }
	//            else if ($(this).text()=="菜单二"){
	//                $(this).parent().next().children(".c2").removeClass("hide").siblings().addClass("hide");
	//            }
	//            else if ($(this).text()=="菜单三"){
	//                $(this).parent().next().children(".c3").removeClass("hide").siblings().addClass("hide");
	//            }
	            //方法二：
	            var name = $(this).attr("f");
	            console.log(name);
	            console.log($("."+name));
	            $("."+name).removeClass("hide").siblings().addClass("hide")
	
	        }
	    }
	</script>
	</html>

六、动态效果

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	
	    </style>
	</head>
	<body>
	<p>lalalalallalalalala</p>
	<img src="http://d17ol771963kd3.cloudfront.net/assets/logo-supreme-f71fe1ba25b4dc78c31dce2cda1178e1.png" alt="">
	<button id="show">显示</button>
	<button id="hide">隐藏</button>
	<button id="toggle">toggle</button>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    //绑定事件 显示消失
	    $("#show").click(function () {
	        $("img").show(1000) //直接调用方法
	    });
	    $("#hide").click(function () {
	        $("img").hide(1000)
	    });
	    $("#toggle").click(function () {
	        $("img").toggle(1000) //等于show and hide合体
	    })
	
	    //滑动
	    $("#slide").click(function () {
	        $("img").slideUp(1000)
	    });
	
	</script>
	</html>


效果2：
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        #con{
	            height: 60px ;
	            text-align: center;
	            background-color: #2459a2;
	            color: white;
	        }
	    </style>
	</head>
	<body>
	<button id="slideDown">slideDown</button>
	<button id="slideUp">slideUp</button>
	<button id="slideToggle">slideToggle</button>
	<div id="con">滑动效果</div>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    $("#slideDown").click(function () {
	        $("#con").slideDown(1000);
	    })
	    $("#slideUp").click(function () {
	        $("#con").slideUp(1000);
	    })
	    $("#slideToggle").click(function () {
	        $("#con").slideToggle(1000);
	    })
	
	</script>
	</html>

效果3：
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        #con{
	
	        }
	    </style>
	</head>
	<body>
	<button id="fadeIn">fadeIn</button>
	<button id="fadeOut">fadeOut</button>
	<button id="fadeToggle">fadeToggle</button>
	<button id="fadeTo">fadeTo</button>
	<div id="con"><img src="http://d17ol771963kd3.cloudfront.net/136481/ma/M5wIC5Vwo1s.png" alt=""></div>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    //替换removeClass addClass
	    //回调函数，显示完成就调用alert(123)
	    $("#fadeIn").click(function () {
	        $("#con").fadeIn(1000,function () {
	            alert(123)
	        });
	    });
	    $("#fadeOut").click(function () {
	        $("#con").fadeOut(1000);
	    });
	    $("#fadeTo").click(function () {
	        $("#con").fadeTo(2000,0.4);//2秒渐变到透明度0.4
	    });
	
	</script>
	</html>

七、结点操作

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	
	<div>
	    <p>PPP</p>
	</div>
	
	</body>
	
	<script src="jquery-3.2.1.js"></script>
	<script>
	    //JS的结点操作
	    //.appendChild(ele)
	    //.removeChild(ele)
	    //.replaceChild(ele_nex, ele_old)
	
	    //jquery结点操作
	    //插入
	    //$("").append("") 插到标签之后
	    //$("p").append("<h1>111</h1>");
	
	    //$("").appendTo("")
	//    var $ele = $("<p>appendto</p>");
	//    $ele .appendTo("div");
	
	    //$("").preppend("")查到标签之前
	    //$("p").prepend("<h1>111</h1>");
	
	    //$("").preppendTo("")
	    //$("<h1>111</h1>").appendTo("p")
	
	    //外部插入(兄弟之间)
	    //after before insertAfter inserBefore
	//    $("div").after("<h1>111</h1>");
	//    $("div").insertAfter("<h1>111</h1>");
	
	    //替换 replaceWith
	//    $("div").replaceWith("<h1>111</h1>");
	
	    //删除
	    //empty:标签还存在  remove
	//    $("div").remove();
	
	    //复制
	    //clone
	    //点击加号增加功能
	    var $a = $("div").clone();
	    $("div").append($a)
	
	</script>
	</html>


clone应用 

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	
	    </style>
	</head>
	<body>
	<div class="box">
	    <div class="item">
	        <input type="button" value="+">
	        <input type="text">
	    </div>
	
	</div>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    $(":button").click(function () {
	        //找到点击的button标签的父节点
	        var $clone = $(this).parent().clone();
	        $clone.children(":button").val("-");
	        $clone.children(":button").attr("onclick","remove_1(this)");
	        $(".box").append($clone);
	    });
	    function remove_1(self) {
	        $(self).parent().remove();
	    }
	</script>
	</html>

八、height and width
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        *{
	            margin:0;
	            padding:0;
	        }
	        .d1{
	            height:200px;
	            width: 200px;
	            background-color: #c461ff;
	            padding: 100px;
	            margin: 50px;
	            border:10px solid blue;
	        }
	    </style>
	</head>
	<body>
	
	<div class="d1">d1d1d1d1d1d1d1d1d1d1</div>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    console.log($(".d1").height()); //200
	    console.log($(".d1").innerHeight());//400 200+padding*2
	    console.log($(".d1").outerHeight());//420 200+padding*2 + border*2
	    console.log($(".d1").outerHeight(true));//520 200+padding*2 + border*2+margin*2
	
	</script>
	</html>

九、CSS 偏移

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        *{
	            margin: 0px;
	        }
	        .b1{
	            height: 200px;
	            width:200px;
	            background-color: #62ff80;
	            position: relative;
	        }
	        .b2{
	            height: 100px;
	            width:100px;
	            background-color: #7190ff;
	            position: absolute;
	        }
	        .b_out{
	            height: 100px;
	            width:100px;
	            background-color: #ff30b5;
	
	        }
	    </style>
	</head>
	<body>
	<h1>偏移量</h1>
	<p class="p1">偏移偏移offset1</p>
	<p class="p2">偏移偏移offset2</p>
	
	<div class="b_out"></div>
	<div class="b1">
	    <div class="b2">
	        <p>position</p>
	    </div>
	</div>
	<button>offset</button>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	//    var $p1o = $(".p1").offset();
	//
	//    var left1 = $p1o.left;
	//    var top1 = $p1o.top;
	//    $(".p2").text(left1+' '+top1);
	//
	//    $("button").click(function () {
	//        $(".p1").offset({left:100,right:200});
	//    })
	
	    var $p1o = $(".b2").position();
	
	    var left1 = $p1o.left;
	    var top1 = $p1o.top;
	    $(".p2").text(left1+' '+top1);
	
	    $("button").click(function () {
	        $(".b2").position({left:100,right:200});
	    })
	
	</script>
	</html>


十、插件

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	<input type="checkbox">
	<input type="checkbox">
	<input type="checkbox">
	<input type="checkbox">
	<input type="checkbox">
	<input type="checkbox">
	<!--点击button,全部选中-->
	<button class="bt1">select</button>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	  //$.ajax
	    $.extend({
	        min:function (a,b) {
	            return a < b ? a : b;
	        },
	        max:function (a,b) {
	            return a > b ? a : b;
	        }
	    });
	    console.log($.min(3,6));
	    console.log($.max(3,6));
	
	//    $("").each()
	    $.fn.extend({
	        cb_all:function () {
	            this.each(function () {
	                this.checked=true;
	            })
	        }
	    });
	  $(".bt1").click(function () {
	      $(":checkbox").cb_all()
	  });
	
	</script>
	</html>


十一、注册功能

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	
	<form action=" " id="form">
	    <input type="text" name="username" class="con" mark="用户名">
	    <input type="password" name="pwd" class="con" mark="密码">
	    <input type="submit" value="submit">
	</form>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    $("#form :submit").click(function () {
	        var flag = true;
	            $("#form .con").each(function () {
	                if($(this).val().trim().length==0){
	                    console.log($(this).next("span").length);
	                    if ($(this).next("span").length != 1){
	                        var mark =  $(this).attr("mark");
	                        var span = $("<span></span>");
	                        span.text(mark+"不能为空");
	                        $(this).after(span);
	                    }
	
	                    flag=false;
	                    return false
	                }
	            });
	        return flag;
	    })
	
	</script>
	</html>

十二、轮播图
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .outer{
	            width: 590px;
	            height: 340px;
	            margin: 20px auto;
	            border: 2px gold solid;
	            position: relative;
	        }
	        ul{
	            list-style-type: none;
	        }
	        ul.img li{
	            position: absolute;
	            top: 0;
	            left:0;
	            display: none;
	        }
	        .icon{
	            position: absolute;
	            bottom: 0px;
	            left: 201px;
	            list-style-type: none;
	
	        }
	        .icon li{
	            display: inline-block;
	            width: 12px;
	            height: 12px;
	            border-radius: 100%;
	            background-color: white;
	            text-align: center;
	            line-height: 12px;
	            margin-left: 10px;
	
	        }
	        .btn{
	            width: 20px;
	            height: 40px;
	            position: absolute;
	            top:150px;
	
	            display: inline-block;
	            background-color: #e0e0e0;
	            text-align: center;
	            line-height: 40px;
	            opacity: 0.6;
	        }
	        .left{
	          left: 0px;
	        }
	        .right{
	            right: 0px;
	        }
	        .icon .active{
	            background-color: #ff6d41;
	        }
	    </style>
	</head>
	<body>
	
	<div class="outer">
	    <ul class="img">
	        <li class="item" style="display: block"><a href=""><img src="https://img13.360buyimg.com/da/jfs/t5938/40/9689321871/142345/c5022a54/59954cb2Ncc04573a.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img1.360buyimg.com/da/jfs/t5794/351/8010595875/83199/37fea79c/5977223aN244fe2ba.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img30.360buyimg.com/da/jfs/t7420/12/508078114/100109/eb7740f2/59940a44Nb2ba898b.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img12.360buyimg.com/da/jfs/t7792/318/623531407/149563/4b090da2/59955c3dN313c278f.jpg" alt=""></a></li>
	    </ul>
	    <ul class="icon">
	        <li class="active"></li>
	        <li></li>
	        <li></li>
	        <li></li>
	    </ul>
	    <div class="left btn"><</div>
	    <div class="right btn">></div>
	</div>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	
	    //自动轮播
	    var i = 0;
	    function move_right() {
	        i++;
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        if (i ==3){
	            i = -1;
	        }
	    }
	    function move_left() {
	        i--;
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        if (i ==-1){
	            i = 3;
	        }
	    }
	    var sin=setInterval(move_right,1000);
	
	    //手动轮播
	    $(".outer").hover(function () {
	        clearInterval(sin);
	    },function () {
	        sin=setInterval(f,1000);
	    });
	
	    $(".icon li").mouseover(function () {
	        var i = $(this).index();
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	    });
	
	    $(".left").click(move_left);
	
	    $(".right").click(move_right);
	</script>
	</html>


十四、滚动条

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	    <style>
	        .outer{
	            width: 590px;
	            height: 340px;
	            margin: 20px auto;
	            border: 2px gold solid;
	            position: relative;
	        }
	        ul{
	            list-style-type: none;
	        }
	        ul.img li{
	            position: absolute;
	            top: 0;
	            left:0;
	            display: none;
	        }
	        .icon{
	            position: absolute;
	            bottom: 0px;
	            left: 201px;
	            list-style-type: none;
	
	        }
	        .icon li{
	            display: inline-block;
	            width: 12px;
	            height: 12px;
	            border-radius: 100%;
	            background-color: white;
	            text-align: center;
	            line-height: 12px;
	            margin-left: 10px;
	
	        }
	        .btn{
	            width: 20px;
	            height: 40px;
	            position: absolute;
	            top:150px;
	
	            display: inline-block;
	            background-color: #e0e0e0;
	            text-align: center;
	            line-height: 40px;
	            opacity: 0.6;
	        }
	        .left{
	          left: 0px;
	        }
	        .right{
	            right: 0px;
	        }
	        .icon .active{
	            background-color: #ff6d41;
	        }
	    </style>
	</head>
	<body>
	
	<div class="outer">
	    <ul class="img">
	        <li class="item" style="display: block"><a href=""><img src="https://img13.360buyimg.com/da/jfs/t5938/40/9689321871/142345/c5022a54/59954cb2Ncc04573a.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img1.360buyimg.com/da/jfs/t5794/351/8010595875/83199/37fea79c/5977223aN244fe2ba.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img30.360buyimg.com/da/jfs/t7420/12/508078114/100109/eb7740f2/59940a44Nb2ba898b.jpg" alt=""></a></li>
	        <li class="item"><a href=""><img src="https://img12.360buyimg.com/da/jfs/t7792/318/623531407/149563/4b090da2/59955c3dN313c278f.jpg" alt=""></a></li>
	    </ul>
	    <ul class="icon">
	        <li class="active"></li>
	        <li></li>
	        <li></li>
	        <li></li>
	    </ul>
	    <div class="left btn"><</div>
	    <div class="right btn">></div>
	</div>
	
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	
	    //自动轮播
	    var i = 0;
	    function move_right() {
	        i++;
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        if (i ==3){
	            i = -1;
	        }
	    }
	    function move_left() {
	        i--;
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        if (i ==-1){
	            i = 3;
	        }
	    }
	    var sin=setInterval(move_right,1000);
	
	    //手动轮播
	    $(".outer").hover(function () {
	        clearInterval(sin);
	    },function () {
	        sin=setInterval(f,1000);
	    });
	
	    $(".icon li").mouseover(function () {
	        var i = $(this).index();
	        $(".icon li").eq(i).addClass("active").siblings().removeClass("active");
	        $(".img li").eq(i).fadeIn(500).siblings().fadeOut(500);
	    });
	
	    $(".left").click(move_left);
	
	    $(".right").click(move_right);
	</script>
	</html>

十五、事件绑定

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>Title</title>
	</head>
	<body>
	<p>12312312</p>
	<ul>
	    <li>11</li>
	    <li>11</li>
	    <li>11</li>
	    <li>11</li>
	    <li>11</li>
	</ul>
	<button class="on">button</button>
	<button class="off">off</button>
	</body>
	<script src="jquery-3.2.1.js"></script>
	<script>
	    //等于window.onload=function(){}，页面执行完之后，再运行代码
	    $(document).ready(function () {
	            $(".on").click(function () {
	        $("ul").append("<li>2222</li>");
	    });
	    //新添加的li标签没有click事件。用on 方法事件委派
	//    $("li").click(function () {
	//        alert(123123);
	//    })
	    $("ul").on("click","li",function () {
	        alert(123123);
	    });
	    //取消委派
	    $(".off").click(function () {
	        $("ul").off();
	    })
	
	    });
	
	</script>
	</html>
	













