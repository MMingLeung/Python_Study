程序介绍：
    使用IO多路复用实现FTP服务器，功能包括：登录、上传、下载、查看服务器目录的文件

程序结构
IO_FTP/
|-----bin/  #执行文件目录
|      |---start.py  #执行程序
|
|-----conf/ #配置文件
|      |---settings.py
|
|-----core/ #核心程序逻辑
|      |---auth.py #用户认证模块
|      |---client.py #客户端模块
|      |---db_handle.py #处理数据模块
|      |---main.py #主逻辑交互程序
|      |---md5_check.py #md5检验模块
|      |---server.py #服务器模块
|      |——-baotou_handler.py #处理报头
|      |——-client_setout.py #与client交互并提供参数
|      |———server_setout.py #与server交互并提供参数
|      |———file_handler.py #文件操作
|      |———roll_bar.py #进度条
|
|-----db/
|     |---person_upload_dir/ #用户上传文件目录
|     |---accounbts.json #用户信息目录
|
|-----docs/ #文档
|
|-----lib/ #库
|
|-----log/ #日志
|
|------README.txt