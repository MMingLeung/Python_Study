# JS 作用域

**变量的作用域在声明时决定！**

### 一、预编译（词法分析）

````javascript
// 
function testA(x, y){
	var x = 100;
  	console.log(x);
    console.log(y);
}

testA(1)

/* 词法分析关注：形式参数、局部变量声明、函数声明(不进行赋值操作)
*  形式参数 x, y: ActiveObject.x = undefined
*			    ActiveObject.y = undefined
* 局部变量声明 x: ActiveObject.x = undefined
*/

/* 执行
*  形式参数 x, y: ActiveObject.x = 1
*			    ActiveObject.y = undefined
* 局部变量声明 x: ActiveObject.x = 100
* 最后打印 100 undefined
*/
````

