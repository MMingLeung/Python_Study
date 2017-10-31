# 一、项目背景

   需要资产自动采集并汇报入库

# 二、目的

1. 实现自动采集服务器信息并入库，减少人工
1. 报障资产信息正确性
1. 便利的信息交换


# 三、架构

1. 资产采集
1. API (接受数据，对外提供数据接口)
1. 后台管理


# 四、重点

1. 资产采集：使用三种不同的方案：agent、paramiko、saltstack，为了提高扩展性，参考django的中间件，以反射的形式，做成插件。
1. API ：参考tonado加密cookie实现加密
1. 后台管理 ：通过配置文件完成增删改查功能


# 五、遇到的问题

1. Linux命令不熟悉
1. 唯一标识
1. API验证

# 六、程序结构

客户端

## 1、目录：
autoclient/  
|———bin/ 可执行文件  
| |——— start.py  主程序  
|  
|——— config/ 自定义配置文件    
|     |——— settings.py 自定义配置文件   
|  
|——— files/ 测试数据  
|  
|——— lib/ 库   
|     |———  config/ 默认配置  
|     |         |——— config.py 初始化配置信息  
|     |         |——— global_settings.py 内置配置信息  
|     |——— convert.py 单位转换程序  
|  
|——— log/ 日志  
|——— src/ 程序功能代码  
|     |——— plugins/ 获取机器信息插件  
|     |         |——— __init__.py 初始化  
|     |         |——— basic/board/cpu/disk/memory/nic 获取机器各项信息的脚本  
|     |  
|     |——— client.py 客户端程序    
|     |———  script.py 程序启动逻辑    

## 2、配置文件  
### 2.1、内置配置文件 global_settings.py 存放程序需要的变量。  
### 2.2、自定义配置文件 settings.py 存放程序需要的根据个人自定义的变量。  
### 2.3、lib/conf/config.py 负责管理配置文件的程序，设置配置。  
            #### 1、根据两个配置文件，循环遍历，写入类的变量中。  
            #### 2、自定义配置文件使用字符串形式导入  

### 3、插件开发  

使用插件获取机器的各项信息  

#### 3.1、方法：agent/ssh(paramiko)/salt 
 
#### 3.2、所需参数
       hostname
       plugin_dict 插件字典
       mode 模式 agent / ssh
       debug 是否调试

#### 3.3、主逻辑
   1、通过配置的字典key:文件名，value是路径。  
   2、通过切分获取类名和路径，使用字符串形式导入获取模块对象  
   3、获取模块对象的类  
   4、做钩子  
   5、实例化类  
   6、调用类里面的方法获取计算机的配置等参数  
       6.1、其中根据类型，调用不同的发送命令的方法 agent/salt/ssh  
       6.2、是否调试模式  
       6.3、客户端agent 直接发送post请求，把信息发给api  
               ssh/salt 获取host列表，再发送  
       6.4、主程序管理6.3  

逻辑整理  
|     |——— plugins/ 获取机器信息插件  
|     |         |——— __init__.py 初始化  
|     |         |——— basic/board/cpu/disk/memory/nic 获取机器各项信息的脚本  
|     |  
|     |——— client.py 客户端程序  
|     |———  script.py 程序启动逻辑  

调用过程：  

    1、start.py — scrpit.run()
        scrpit.run()
        根据配置文件里面的MODE选择模式（AGENT,SSHSALT），运行其execute方法
    2、client.py
        建立基类，定义一个发送资产的方法
        AGENT、SSHSALT继承基类，根据这两种模式分别定义方法。
        AGENT：根据唯一标识发送本地计算机硬件信息
        SSHSALT:先发送GET请求获取host列表，根据host列表，使用多线程调用run方法发送服务器信息


#### 3.4、各项获取信息的代码

1、系统信息

2、主板信息

3、CPU信息

4、硬盘信息

5、网卡信息




### 4、唯一标识
   如果以SN号作为唯一标识，所采集的机器是物理机可以，如果有虚拟机则出现问题。
   SSH/SALT不存在唯一标识，采集主机名由API发送给中控机。
      
   AGENT在发送数据前，需要作唯一标识的判断，方法如下：
            a.需要将新服务器基本信息先录入CMDB
            b.装机时，设置主机名
            c.第一次采集：本地文件不存在或内容为空，执行主机名写入，发送至API
            d.第n次采集：主机名文件中获取，发送API
def execute(self):
    server_info = PluginsManage().execute_plugin()
    hostname = server_info['basic']['data']['hostname']
    cert = open(settings.CERT_PATH, 'r', encoding='utf8').read()
    #第一次写入
    if not cert.strip():
        with open(settings.CERT_PAT, 'r', encoding='utf8') as f
            f.write(hostname)
    else:
        #以本地文件为准
        server_info['basic']['data']['hostname'] = cert
    self.post_asset(server_info)



### 5、线程池的使用
  SSHSLAT在发送数据给API时，实现并发。
def run(self, host):
    server_info = PluginsManage(host).execute_plugin()
    self.post_asset(server_info)
   

def execute(self):
    host_list = self.get_host()
    p = ThreadPoolExecutor(20)
    for host in host_list:
        p.submit(self.run, host)


### 6、API验证
传输过程中，保证数据不会被修改，参考tornado加密cookie

步骤：
   客户端

	1. key（自定义的，服务器和客户端相同）和时间进行md5加密
	2. 利用刚生成的md5和时间戳拼接
	3. 在请求头中的OpenKey中


   服务端

	1. 从请求头重获取HTTP_OPENKEY（名字自动转换成这个名字），切分，前半部分是md5值，后半部分是客户端发送的时间。
	2. 根据key和客户端发来的时间生成一个md5与客户端的进行匹配。
	3. 时间检测

		1. 获取服务器接受时的时间 - 客户端发送过来的时间，如果大于设定值报错，证明有人保存了这个OPENKEY再一次发送。
	4. 已使用md5值检测

		1. 在数据库中保存已使用的md5表，进行对比。
	5. 维护数据库md5的表，存放md5和其过期时间，服务器时间大于过期时间就删除。

#### api验证

	def auth():
	
	key = settings.AUTH_KEY
	ctime = time.time()
	new_key = "%s|%s" % (key, ctime)
	m = hashlib.md5()
	m.update(bytes(new_key, encoding='utf8'))
	md5_key = m.hexdigest()
	md5_key_time = "%s|%s" % (md5_key, ctime)
	
	return md5_key_time

##### server 验证装饰器
	
	api_key_record = {}
	                                            #超时时间
	# {'eqwqweqwewqeqwew|213123123.123':'321321321.32131'}
	#验证规则装饰器
	def auth(func):
	    def wrapper(request, *args, **kwargs):
	        # 方法1改进：
	        client_md5_key_time = request.META.get('HTTP_OPENKEY')
	        print(client_md5_key_time)
	        client_md5_key, client_ctime = client_md5_key_time.split('|')
	        server_time = time.time()
	        # 时间检测
	        if server_time - float(client_ctime) > 10:
	            return HttpResponse('时间检测 非法')
	        # 列表检测
	        if client_md5_key in api_key_record:
	            return HttpResponse('列表检测 非法')
	        else:
	            api_key_record[client_md5_key_time] = float(client_ctime) + 10
	        # key——time检测
	        temp = "%s|%s" % (settings.AUTH_KEY, client_ctime)
	        m = hashlib.md5()
	        m.update(bytes(temp, encoding="utf8"))
	        server_md5_key = m.hexdigest()
	        if server_md5_key != client_md5_key:
	            return HttpResponse('无法访问')
	        elif server_md5_key == client_md5_key:
	            res = func(request)
	            return HttpResponse(res)
	        # 超时的md5需要删除
	        for k in list(api_key_record.keys()):
	            v = api_key_record[k]
	            if server_time > v:
	                del api_key_record[k]
	    return wrapper


### 7、传输数据加密

	Crypto加密
	
	client
	
	def encrypt(message):
	    key = settings.OPEN_KEY #长度有限制16个字节
	    cipher = AES.new(key, AES.MODE_CBC, key)
	    # bytearray 字节数组
	    message = json.dumps(message)
	    ba_data = bytearray(message, encoding='utf-8’)
	
	    #构建长度等于16个字节的倍数的字节数组
	    len1 = len(ba_data) #总长度
	    len2 = len1 % 16 #求余，得出还需要增加的个数
	    if len2 == 0:
	        need_add = 16 #余数为零加16个
	    else:
	        need_add = 16 - len2
	    for i in range(need_add):
	        ba_data.append(need_add) #bytesarray只能加ASCII数字
	    final_data = ba_data.decode('utf-8')
	    msg = cipher.encrypt(final_data) #要加密的字符串必需是16个字节的倍数
	    return msg
	
	server
	
	def decrypt(message):
	
	    key = settings.OPEN_KEY
	    cipher = AES.new(key, AES.MODE_CBC, key)
	    result = cipher.decrypt(message)
	    #result[-1] 代表添加的个数也是添加的内容
	    #取开头到倒数添加个数的位置
	    data = result[0:-result[-1]]
	    #把字节转换为字符串
	    data = str(data, encoding='utf-8')
	
	    return data


服务端
### 8、数据库设计


### 9、入库

    插件的形式进行入库操作（反射）






### 10、后台管理

#### 10.1、 动态生成表格的标题和数据
	
	步骤：
	1、构建数据
	GET请求
	#视图函数全部代码
	def curd_json(request):
	    if request.method == 'DELETE':
	        id_list = json.loads(str(request.body, encoding='utf8'))
	        print(id_list)
	        return HttpResponse('123')
	    elif request.method == 'POST':
	        pass
	    elif request.method == 'GET':
	    # 1
	    # 无法序列化时间
	    # json 扩展支持时间序列化
	        class JsonCustomEncoder(json.JSONEncoder):
	            def default(self, filed):
	                if isinstance(filed, datetime):
	                    return filed.strftime('%Y-%m-%d %H:%M:%S')
	                elif isinstance(filed, date):
	                    return filed.strftime('%Y-%m-%d')
	                else:
	                    return json.JSONEncoder.default(self, filed)
	
	        # ==========================
	        table_config = [
	            {'q': None,   #数据库查询字段
	             'title': '', #标题
	             'display': True, #是否显示
	             'text': {     #内容
	                 'tpl': '<input type="checkbox" value="{n1}">',
	                 'kwargs': {'n1': '@id'}
	             },
	             'attrs': {'nid': '@id'},#td标签的属性
	             },
	            {'q': 'id',
	             'title': 'ID',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@id'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@id'},
	             },
	            {'q': 'hostname',
	             'title': '主机名',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@hostname'}
	             },
	             'attrs': {'edit-enable': 'true', 'k2': '@hostname'},
	             },
	            {'q': 'create_at',
	             'title': '创建时间',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@create_at'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@create_at'},
	             },
	            {'q': 'asset__cabinet_num',
	             'title': '机柜号',
	             'display': True,
	             'text': {
	                 'tpl': 'BJ-{n1}',
	                 'kwargs': {'n1': '@asset__cabinet_num'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__cabinet_num'},
	             },
	            {'q': 'asset__business_unit__name',
	             'title': '业务线',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@asset__business_unit__name'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__name'},
	             },
	            {'q': 'asset__business_unit__id',
	             'title': '业务线ID',
	             'display': False,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@asset__business_unit__id'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__id'},
	             },
	            # 页面显示：  标题：操作    删除、编辑（a标签）
	            {'q': None,
	             'title': '操作',
	             'display': True,
	             'text': {
	                 'tpl': '<a href="/del?nid={n1}">删除</a>',
	                 'kwargs': {'n1': '@id'}
	             },
	             },
	        ]
	        # @+id 数据库中取值
	        search_config = [
	            {'name': 'hostname__contains', 'text': '主机名', 'condition_type': 'input'},
	            # 模糊匹配
	            {'name': 'create_at', 'text': '创建时间', 'condition_type': 'input'},
	            {'name': 'asset__cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
	        ]
	        # ========获取搜索条件========
	        condition = request.GET.get('condition')
	        print(condition)
	        condition_dict = json.loads(condition)
	        # 最外面的Q
	        con = Q()
	        for name, values in condition_dict.items():
	            ele = Q()  # select * from where xx=1 or xx=2
	            ele.connector = 'OR'
	            for item in values:
	                ele.children.append((name, item))
	            con.add(ele, 'AND')
	            # ===============
	        values_list = []
	        for row in table_config:
	            if not row['q']:
	                continue
	            values_list.append(row['q'])
	        v = models.Server.objects.filter(con).values(*values_list)
	        ret = {
	            'table_config': table_config,
	            'server_list': list(v),
	            'search_config':search_config,
	        }
	        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))



	自定义数据结构
	{'q':数据库查询的字段，
	 'title':标题,
	'display':显示, 
	'text':{'tpl':标签, 
	'kwargs':{'n1':@id} },  
	'attrs':{'nid':'@id'} 
	 }
	table_config = [
	            {'q': None,   #数据库查询字段
	             'title': '', #标题
	             'display': True, #是否显示
	             'text': {     #内容
	                 'tpl': '<input type="checkbox" value="{n1}">',
	                 'kwargs': {'n1': '@id'}
	             },
	             'attrs': {'nid': '@id'},#td标签的属性
	             },
	
	            {'q': 'id',
	             'title': 'ID',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@id'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@id'},
	             },
	
	            {'q': 'hostname',
	             'title': '主机名',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@hostname'}
	             },
	             'attrs': {'edit-enable': 'true', 'k2': '@hostname'},
	             },
	
	            {'q': 'create_at',
	             'title': '创建时间',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@create_at'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@create_at'},
	             },
	
	            {'q': 'asset__cabinet_num',
	             'title': '机柜号',
	             'display': True,
	             'text': {
	                 'tpl': 'BJ-{n1}',
	                 'kwargs': {'n1': '@asset__cabinet_num'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__cabinet_num'},
	             },
	
	            {'q': 'asset__business_unit__name',
	             'title': '业务线',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@asset__business_unit__name'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__name'},
	             },
	
	            {'q': 'asset__business_unit__id',
	             'title': '业务线ID',
	             'display': False,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@asset__business_unit__id'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__id'},
	             },
	
	            # 页面显示：  标题：操作    删除、编辑（a标签）
	            {'q': None,
	             'title': '操作',
	             'display': True,
	             'text': {
	                 'tpl': '<a href="/del?nid={n1}">删除</a>',
	                 'kwargs': {'n1': '@id'}
	             },
	             },
	        ]

	#传至html页面的数据
	 ret = {
	            'table_config': table_config,
	            'server_list': list(v),
	            'search_config':search_config,
	        }

#### HTML处理

##### 一、初始化

	        1、初始化函数initail()
	        2、如果是刷新就把搜索条件清空，否则把搜索条件传到后台
	        3、初始化头部
	                根据自定义数据结构tableconfig，判断display是否为True，对应生成tr 和 th，并赋值
	        4、初始化内容
	                循环遍历server_list 服务器数据
	                循环遍历tableconfig，创建tr,根据display，创建td，为td设置属性。（根据自定义规则@+字段）
	                td内容赋值。
	                        tableconfig使用里面的'tpl', 'kwargs'，kwargs先要把自定义规则的值获取到。
	                        循环遍历text.kwargs ,把其中的value赋值给一个变量（后面判断如果有@或@@就替换）
	                                如果开头是@@， 上层循环是tableconfig，rrow.q 获取这个kwargs的q值也就是数据库名字，上上层循环是
	                                server_list , row[rrow.q]获取其数据库字段的值，然后跟全局变量choices进行判断替换@@ 的值
	                                如果开头是@ ，  使用上上层循环row[去掉@之后的字段]取值替换    
	                 最后new 一个变量存放内容并且格式化tpl的值
	                 把内容加到td innerText中，td加到tr中，tr加到tbody中              

###### 1、自执行函数

	(function (jq) {
	...
	})(jQuery);

###### 2、扩展

	jq.extend({
	xx: function (url) {
	....
	}
	})

##### #3、初始化

	initial(url);
	        //REFREASH默认是false ，页面第一次读取时，搜索框为空
	        // 执行函数，获取当前搜索条件
	        if (REFREASH){
	            var searchCondition = {}
	        }else {
	            //把搜索框的值组合成字典赋值给变量
	             var searchCondition = getSearchCondition();
	            console.log(searchCondition);
	        }
	        $.ajax({
	            url: url,
	            type: 'GET',  //获取数据
	            dataType: 'JSON',
	            data:{condition:JSON.stringify(searchCondition)},
	            success: function (res) {
	                $.each(res.global_dict, function (k, v) {
	                    #把返回的值放入全局变量
	                    GLOBAL_DICT[k] = v
	                });
	                /*
	                 'table_config': table_config,
	                 'server_list': list(v),
	                 'global_dict': {
	                 'device_status_choices': models.Asset.device_status_choices,
	                 'device_type_choices': models.Asset.device_type_choices,
	                 }
	                 */
	                //执行三个初始化，生成标题，内容
	                initTableHeader(res.table_config);
	                initTableBody(res.server_list, res.table_config);
	                initSearch(res.search_config);
	            }
	        })
	    }
	


###### 4、searchCondition

	// 返回搜索条件
	    function getSearchCondition() {
	        var condition = {};
	        $('.search-list').find('input[type="text"],select').each(function () {
	            //select框或者input框
	            var name = $(this).attr('name');
	            var value = $(this).val();
	            if (condition[name]) {
	                condition[name].push(value)
	            } else {
	                condition[name] = [value];
	            }
	        });
	        return condition
	    }

##### 5、initTableHeader

	function initTableHeader(tableConfig) {
	        /*
	           {'q': 'id',
	             'title': 'ID',
	             'display': True,
	             'text': {
	                 'tpl': '{n1}',
	                 'kwargs': {'n1': '@id'}
	             },
	             'attrs': {'k1': 'v1', 'k2': '@id'},
	             },
	         */
	        #找到表格的头部
	        $('#tbHeader').empty();
	        #创建tr
	        var tr = document.createElement('tr');
	        #循环遍历数据
	        $.each(tableConfig, function (k, v) {
	            if (v.display) {
	                #创建th
	                var tag = document.createElement('th');
	                #赋值给标签的内容，作为显示结果
	                tag.innerHTML = v.title;
	                #添加到tr里面
	                $('#tbHeader').find('tr').append(tag)
	                #
	                $(tr).append(tag)
	            }
	        });
	        $('#tbHeader').append(tr);
	    }


##### 6、initTableBody 初始化表格内容

	$('#tbBody').empty();
	
	        #serverList ：后台查询出来的结果
	        $.each(serverList, function (k, row) {
	            /*
	
	             *  k = 0 row = {hostname: "c1.com", id: 1, create_at: "2017-10-02 05:00:55"}
	
	             0:{hostname: "c1.com", id: 1, create_at: "2017-10-02 05:00:55"}
	
	             * */
	            //
	
	            #创建标签
	            var tr = document.createElement('tr');
	
	            #属性赋值
	            tr.setAttribute("nid", row.id);
	
	      #循环遍历tableConfig
	            $.each(tableConfig, function (kk, rrow) {
	                /*
	                 k = 0: row = {q: "id", title: "ID"} // row.q = id
	                  /*
	                           {'q': 'id',
	                         'title': 'ID',
	                         'display': True,
	                         'text': {
	                             'tpl': '{n1}',
	                             'kwargs': {'n1': '@id'}
	                         },
	                         'attrs': {'k1': 'v1', 'k2': '@id'},
	                         },
	                 */
	                #根据tableConfig（自定制的格式），显示为TRUE
	                if (rrow.display) {
	
	                   #创建td 存放内容
	                    var td = document.createElement('td');
	
	                    #自定义的两个规则：1、@+字段表示取值 2、@@+字段表示获取choice数据的值
	                    $.each(rrow.attrs, function (atkey, atval) {
	                        /*
	                             'attrs': {'k1': 'v1', 'k2': '@id'},
	                        */
	                        //判断如果是@ + XX取真实的值
	                        if (atval[0] == '@') {
	                            //取到id的值                row：{hostname: "c1.com", id: 1, create_at: "2017-10-02 05:00:55"}   substring切分
	                            td.setAttribute(atkey, row[atval.substring(1, atval.length)])
	                        } else {
	                            td.setAttribute(atkey, atval)
	                        }
	                    });
	
	
	                    //@id变更 rrow.text.kwargs: {'n1':'1', 'n2':'123'}#}
	                    /*rrow.text.kwargs:
	                             'kwargs': {'n1': '@id'}
	                    */
	                    var newKwargs = {};
	                    $.each(rrow.text.kwargs, function (j, k) {
	                        //j: n1  k:@id
	                        var aValue = k;
	
	                        //'kwargs': {'n1': '@@device_type_choices'}
	                        //自定义规则 @@ + id 等于选择choice
	                        if (k.substring(0, 2) == '@@') {
	                            var global_key = k.substring(2, k.length);
	
	                            //device_type_id
	                            //获取device_type_id的值
	                            //   rrow.q = 'device_type_id' 字段名 ，row[device_type_id] ：查询结果中的choices选项id值
	                            var did = row[rrow.q];
	
	                            //GLOBAL_DICT[global_key] choice字典
	                            $.each(GLOBAL_DICT[global_key], function (gk, gv) {
	                                if (gv[0] == did) {
	                                    aValue = gv[1];
	                                }
	                            })
	                        }
	                        
	           #自定义规则取值
	                        else if (k[0] == '@') {
	                            //取到id的值
	                            aValue = row[k.substring(1, k.length)]
	                        }
	                        newKwargs[j] = aValue;
	                    });
	
	          //   'tpl': '<input type="checkbox" value="{n1}">'
	                    var newText = rrow.text.tpl.format(newKwargs);
	
	                    //内容赋值
	                    td.innerHTML = newText;
	                    tr.append(td)
	                }
	            });
	            $('#tbBody').append(tr);
	        });
	    }


##### 7、初始化搜索框的下拉栏

	  function initSearch(searchConfig) {
	        //只需要生成一次
	        if (searchConfig && SEARCH_FLAG) {
	            SEARCH_FLAG = false;
	
	            //找到searchArea ul
	            $.each(searchConfig, function (k, v) {
	                /*自定义的数据
	                 search_config = [
	                 {'name': 'carbinet_num', 'text': '机柜号', 'condition_type': 'input'},
	                 {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_choices'},
	                 {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select',
	                 'global_name': 'device_status_choices'},
	                 ]
	                 */
	
	                var li = document.createElement('li');
	                var a = document.createElement('a');
	                a.innerHTML = v.text;
	                $(li).append(a);
	                $(li).attr('condition_type', v.condition_type);
	                $(li).attr('name', v.name);
	                if (v.condition_type == 'select') {
	                    $(li).attr('global_name', v.global_name);
	                }
	                $('.searchArea ul').append(li)
	            });
	
	            //初始化默认配置
	            //searchConfig[0]初始化
	            $('.search-item .searchDefault').text(searchConfig[0].text);
	            //如果第一条是select标签， 属性赋值，遍历全局变量字典，赋值text和val
	            if (searchConfig[0].condition_type == 'select') {
	                var sel = document.createElement('select');
	                $(sel).attr('class', 'form-control');
	                $(sel).attr('name', searchConfig[0].name);
	                $.each(GLOBAL_DICT[searchConfig[0].global_name], function (k, v) {
	                    var op = document.createElement('option');
	                    $(op).text(v[1]);
	                    $(op).val(v[0]);
	                    $(sel).append(op);
	                });
	                //select 框加入到该div中
	                $('.input-group').append(sel)
	            } else {
	                var inp = document.createElement('input');
	                $(inp).attr('name', searchConfig[0].name);
	                $(inp).attr('type', 'text');
	                $(inp).attr('class', 'form-control');
	                //ipt加入到该div中
	                $('.input-group').append(inp)
	            }
	        }
	    }


### 二、进入退出编辑模式

可编辑的标签在初始化的时候加入了属性'edit-enable'=true， 'edit-type'=select or input

1、进入编辑模式

     1、找到全部含有'edit-true' =true的tr标签
     2、获取edit-tpye属性
     3、如果是select ，获取原来的值。创建select标签,获取choices数据库的值，循环遍历choices，创建option标签，如果等于原
            来的值，在属性加入选中状态，最后option加入到select 中，select 放入 tr中
     4、如果是input , 获取原来的文本信息，创建inp ，放入tr中

2、退出编辑模式

    1、找到编辑属性为true的tr标签，循环遍历
    2、如果是select , 找到select标签转变成DOM 对象，调用selectOptions获取选中的值的文本值，放入td标签的html中。在td标
        签中加入newOrigin属性值是新选中的option标签的val
    3、如果是inp ,把input文本内容赋值给td的html中

	function trIntoEdit($tr) {
	
	        //找到所有的td标签且edit-enable="true"
	        $tr.find('td[edit-enable="true"]').each(function () {
	            var editType = $(this).attr('edit-type');
	            if (editType == 'select') {
	                //生成下拉框:找到数据源
	                //默认选中原来的值
	                var origin = $(this).attr('origin'); //原来的值
	
	                //该choices值的数据
	                var deviceTypeChoices = GLOBAL_DICT[$(this).attr('global-key')];
	
	                //生成select标签
	                var selectTag = document.createElement('select');
	                $.each(deviceTypeChoices, function (k, v) {
	                    var option = document.createElement('option');
	                    $(option).text(v[1]);
	                    $(option).val(v[0]);
	                    if (v[0] == origin) {
	                        $(option).prop('selected', true);
	                    }
	                    $(selectTag).append(option)
	                });
	                //放到td中
	                $(this).html(selectTag);
	            } else {
	                var v1 = $(this).text(); //循环的每一个td,获取文本信息
	                var inp = document.createElement('input');
	                $(inp).val(v1);
	                //input标签替换原来的内容
	                $(this).html(inp);
	            }
	        })
	    }
	    function trOutEdit($tr) {
	        //找到所有的td标签且edit-enable="true"
	        $tr.find('td[edit-enable="true"]').each(function () {
	            var editType = $(this).attr('edit-type');
	            if (editType == 'select') {
	                //DOM对象
	                //select选中的对象
	                var option = $(this).find('select')[0].selectedOptions;
	                //select选中的对象的值放入td标签中
	                $(this).html($(option).text());
	                //用于编辑保存时对比旧值
	                $(this).attr('newOrigin', $(option).val())
	            } else {
	                var inputVal = $(this).find('input').val();
	                //input标签替换原来的内容
	                $(this).html(inputVal);
	            }
	        })
	    }
	
	
	1、如果是在编辑模式btn-warning， 文本内容改变去掉样式，找到所有checkbox标签，调用离开编辑模式的函数
	
	#点击事件
	            $('#InOutEditMode').click(function () {
	                if ($(this).hasClass('btn-warning')) {
	                    //exit edit
	                    $(this).removeClass('btn-warning');
	                    $(this).text('进入编辑模式');
	                    $("#tbBody").find(':checkbox').each(function () {
	                        if ($(this).prop('checked')) {
	                            //checkbox 找到tr标签
	                            var $tr = $(this).parent().parent();
	                            trOutEdit($tr);
	                        }
	                    });
	                } else {
	                    //enter edit
	                    $(this).addClass('btn-warning');
	                    $(this).text('退出编辑模式');
	                    $("#tbBody").find(':checkbox').each(function () {
	                        if ($(this).prop('checked')) {
	                            var $tr = $(this).parent().parent();
	                            trIntoEdit($tr);
	                        }
	                    });
	                }
	            });


### 三、checkbox全选、反选、取消

全选
1、找到全部checkbox标签，循环遍历，如果是进入编辑模式就调用进入模式函数并且checked属性为true  

2、否则只是设置checked属性为true

	$('#checkAll').click(function () {
	            
	                if ($('#InOutEditMode').hasClass('btn-warning')) {
	                    $('#tbBody').find(':checkbox').each(function () {
	                        if (!$(this).prop('checked')) {
	                            var $tr = $(this).parent().parent();
	                            trIntoEdit($tr);
	                            $(this).prop('checked', true)
	                        }
	                    })
	                } else {
	                    $('#tbBody').find(':checkbox').prop('checked', true)
	                }
	            });

反选
1、如果是编辑模式，先退出编辑模式，在设置checked属性为false，反之。

	$('#checkReverse').click(function () {
	                if ($('#InOutEditMode').hasClass('btn-warning')) {
	                    $('#tbBody').find(':checkbox').each(function () {
	                        var $tr = $(this).parent().parent();
	                        if ($(this).prop('checked')) {
	                            var $tr = $(this).parent().parent();
	                            trOutEdit($tr);
	                            $(this).prop('checked', false)
	                        } else {
	                            if (!$(this).prop('checked')) {
	                                var $tr = $(this).parent().parent();
	                                trIntoEdit($tr);
	                                $(this).prop('checked', true)
	                            }
	                        }
	                    })
	                } else {
	                    $('#tbBody').find(':checkbox').each(function () {
	                        var $tr = $(this).parent().parent();
	                        if ($(this).prop('checked')) {
	                            $(this).prop('checked', false)
	                        } else {
	                            if (!$(this).prop('checked')) {
	                                $(this).prop('checked', true)
	                            }
	                        }
	                    })
	                }
	            });
	
	取消
	            $('#checkCancel').click(function () {
	                // $('#tbBody').find(':checkbox').prop('checked', false)
	                // //退出编辑模式
	                // $('#tbBody').find('tr').each(function () {
	                //     trIntoEdit($(this));
	                // })
	                if ($('#InOutEditMode').hasClass('btn-warning')) {
	                    $('#tbBody').find(':checkbox').each(function () {
	                        if ($(this).prop('checked')) {
	                            var $tr = $(this).parent().parent();
	                            trOutEdit($tr);
	                            $(this).prop('checked', false)
	                        }
	                    })
	                } else {
	                    $('#tbBody').find(':checkbox').prop('checked', false)
	                }
	            });


### 三、删除

          
                 $('#mulDelete').click(function () {
                //找到被选中的
                var idList = [];
                $('#tbBody').find(':checked').each(function () {
                    //放入list中
                    idList.push($(this).val());
                });
                $.ajax({
                    url: url,
                    type: 'delete',
                    data: JSON.stringify(idList),
                    success: function (arg) {
                        // console.log(arg)
                    }
                })
            });

### 四、保存

1、先退出编辑模式
2、获取tr的nid（这条数据的id），遍历tr的子标签，如果eidt-type=select,获取新值和旧值，如果不相等，对应的name和值放到
    一个字典中，如果是inpt框，同上，新旧值对比，不相等才赋值。
3、根据flag(有改动flag为true)，字典加入id.并把字典放入列表中，以put方法发送到后台
4、后台反序列化后得到一个列表包字典，pop 出id的值作为filter的条件， 其余作为update参数

       $('#checkSave').click(function () {
                //退出编辑模式
                if ($('#InOutEditMode').hasClass('btn-warning')) {
                    $('#tbBody').find(':checkbox').each(function () {
                        if ($(this).prop('checked')) {
                            var $tr = $(this).parent().parent();
                            trOutEdit($tr);
                            $(this).prop('checked', false)
                        }
                    })
                }
                //获取数据发到后台
                var all_list = [];
                $('#tbBody').children().each(function () {
                    //tr对象
                    var $tr = $(this);
                    var nid = $tr.attr('nid');
                    //找edit-enable = true
                    var row_dict = {};
                    var flag = false;
                    $tr.children().each(function () {
                        if ($(this).attr('edit-enable')) {
                            if ($(this).attr('edit-type') == 'select') {
                                //下拉框的保存
                                var newData = $(this).attr('newOrigin');
                                var oldData = $(this).attr('origin');
                                if (newData) {
                                    if (newData != oldData) {
                                        var name = $(this).attr('name');
                                        row_dict[name] = newData;
                                        flag = true;
                                    }
                                }
                            } else {
                                //input框的保存
                                var newData = $(this).text();
                                var oldData = $(this).attr('origin');
                                if (newData != oldData) {
                                    var name = $(this).attr('name');
                                    row_dict[name] = newData;
                                    flag = true;
                                }
                            }
                        }
                    });
                    if (flag) {
                        row_dict['id'] = nid;
                    }
                    all_list.push(row_dict);
                });
                //ajax 请求
                $.ajax({
                    url: url,
                    type: 'PUT',
                    data: JSON.stringify(all_list),
                    success: function (arg) {
                        // console.log(arg)
                    }
                })
            });



### 五、搜索框的下拉栏

委托形式绑定，用于元素不是一开始存在情况

1、找到li标签，也就是下拉栏
2、默认框修改属性
3、如果是select框生成新的select和option
4、删除旧的输入框
5、添加新的
$('.search-list').on('click', 'li', function () {
                //文本信息
                var wenben = $(this).text();
                var name = $(this).attr('name');
                var globalName = $(this).attr('global_name');
                var conditinType = $(this).attr('condition_type');

     
                //li父节点ul的上一个节点寻找.searchDefault改变文本
                $(this).parent().prev().find('.searchDefault').text(wenben);

                if (conditinType == 'select') {
                    //输入框
                    var sel = document.createElement('select');
                    //列表[1,xx],[2,bb],生成option
                    $(sel).attr('class', 'form-control');
                    $(sel).attr('name', name);
                    $.each(GLOBAL_DICT[globalName], function (k, v) {
                        var op = document.createElement('option');
                        $(op).text(v[1]);
                        $(op).val(v[0]);
                        $(sel).append(op);
                    });
                    //移除原来的input或者select框，然后加入该次选择的内容的inp或sle框
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(sel);
                } else {
                    var inp = document.createElement('input');
                    $(inp).attr('class', 'form-control');
                    $(inp).attr('name', name);
                    $(inp).attr('type', 'text');
                    $(this).parent().parent().next().remove();
                    $(this).parent().parent().after(inp);
                }
            })

### 六、搜索框添加、删除

1、找到search-list

2、修改图标,添加class

3、添加到search-list中

            $('.search-list').on('click', '.addSearchCondition', function () {
                //找到search-item 拷贝新的搜索项
                var newSearcheItem = $(this).parent().parent().clone();
                $(newSearcheItem).find('.addSearchCondition span').removeClass('glyphicon glyphicon-plus').addClass('glyphicon glyphicon-minus');
                $(newSearcheItem).find('.addSearchCondition').addClass('del').removeClass("addSearchCondition");
                $('.search-list').append(newSearcheItem);
            });

            $('.search-list').on('click', '.del', function () {
                //由当前按钮找到整个search-item 删除
                $(this).parent().parent().remove()
            });


七、后台处理

DELETE请求



PUT请求



GET请求

1、


def get_data_list(model_cls, request, table_config):
    #用于filter查询的
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])
    # ========获取搜索条件========
    condition = request.GET.get('condition')
    print(condition)
    {"device_status_id":["1","2"]}
    condition_dict = json.loads(condition)
    # 最外面的Q
    con = Q()
    for name, values in condition_dict.items():
        ele = Q()  # select * from where xx=1 or xx=2
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name, item))
        con.add(ele, 'AND')
    # ===============
    v = model_cls.objects.filter(con).values(*values_list)
    return v

def asset_json(request):

    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf8'))
        print(id_list)
        return HttpResponse('123')
    elif request.method == 'PUT':
        all_list = json.loads(str(request.body, encoding='utf8'))
        print(all_list)
        for row in all_list:
            nid = row.pop('id')
            models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('123')

    elif request.method == 'GET':
        # 1
        # 无法序列化时间
        # json 扩展支持时间序列化
        class JsonCustomEncoder(json.JSONEncoder):
            def default(self, filed):
                if isinstance(filed, datetime):
                    return filed.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(filed, date):
                    return filed.strftime('%Y-%m-%d')
                else:
                    return json.JSONEncoder.default(self, filed)

        v = get_data_list(models.Asset, request, ASSET_CONFIG.table_config)
        print(v)
        ret = {
            'table_config': ASSET_CONFIG.table_config,
            'server_list': list(v),
            'global_dict': {
            'device_status_choices': models.Asset.device_status_choices,
            'device_type_choices': models.Asset.device_type_choices,
            'idc_choices':list(models.IDC.objects.values_list('id', 'name')),
            },
            'search_config': ASSET_CONFIG.search_config,
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))



POST请求
