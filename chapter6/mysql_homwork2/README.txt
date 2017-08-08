程序介绍：
    使用SQLAlchemy + pymysql 设计的用户管理程序，包含注册、登录、找回密码功能，管理者能增、删、改其他用户信息及分配权限。

程序结构
mysql_homwork/
|-----bin/  #执行文件目录
|      |---start.py  #执行程序
|
|-----core/ #核心程序逻辑
|      |---login.py #用户认证模块
|      |---main.py #主逻辑交互程序
|      |---register.py # 注册功能接口
|      |---retrieve_password #找回密码功能接口
|
|-----db/
|     |---mysql_bak.sql #数据库
|
|-----docs/ #文档
|
|-----lib/ #库
|      |---db_handler.py # 数据库交互程序
|      |---permission_manager.py # 权限管理程序
|      |---user_manager.py # 用户管理程序
|
|-----log/ #日志
|
|------README.txt