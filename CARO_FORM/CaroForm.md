# 自定义Form 组件

## 简介：

&emsp;&emsp;本组件为 Tornado 框架提供类似 Django Form 组件的字段验证及生成 html 标签功能。

<br>

- [快速使用](#1)

- [系统详解](#2)

  - [架构](#2_1)
  - [程序目录结构](#2_2)
  - [组件功能及原理](#2_3)

  <br>

## <a id='1'>快速使用</a>：

### 1、环境

#### Python: 3.5

#### Packages:

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

```python
# requirement.txt
tornado==4.5.3
```



### 2、试用

&emsp;&emsp;运行 apps.py， 输入 url ，进入测试页面

&emsp;&emsp;

<br>

**整体效果**：

![https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/form_initialize_index.png?raw=true]()

<br>

**默认值**：

![https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/default_value.png?raw=true]()

![https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/multi_select_default.png?raw=true]()

<br>

**错误提示：**

1. 默认错误提示

![https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/origin_error_msg.png?raw=true]()

2. 自定义错误提示

![https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/customize_error_msg.png?raw=true]()



