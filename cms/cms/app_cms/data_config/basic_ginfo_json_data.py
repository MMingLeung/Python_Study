'''
table_config 
    前端通过该配置生成对应的表格头部及内容信息
    'q':作为数据库字段查询
    'title':表格标题
    'display':是否显示
    'text':{
        'tpl':html模板
        'kwargs':用于html模板参数格式化。自定义规则：@+字段取值，@@+字段取全局变量字典的值。
    }
    'attrs':html标签的属性
        {  'edit-enable': 标签是否能编辑
           'origin': 保存原始值，用于跟新值作比较
        }

motai_config
    前端通过该配置生成对应的模态对话框实现添加功能
    'title': 标题
    'display': 是否显示
    'attrs': 标签属性

search_config
    前端通过该配置生成对应的搜索框
    'name': 标签属性
    'text': 下拉框文本
    'condition_type': 输入框类型input/select

'''


table_config = [
                {'q': None,  # 数据库查询字段
                 'title': '',  # 标题
                 'display': True,  # 是否显示
                 'text': {  # 内容
                     'tpl': '<input type="checkbox" value="{n1}">',
                     'kwargs': {'n1': '@id'}
                 },
                 'attrs': {'nid': '@id'},  # td标签的属性
                 },

                {'q': 'id',
                 'title': 'ID',
                 'display': True,
                 'text': {
                     'tpl': '{n1}',
                     'kwargs': {'n1': '@id'}
                 },
                 'attrs': { 'id': '@id'},
                 },
                {
                    'q':'title',
                    'title':'组名',
                    'display':True,
                    'text':{
                        'tpl':'<a href="/backend/basic_ginfo.html?md=detail&nid={n1}">{n2}</a>',
                        'kwargs':{'n1':'@id', 'n2':'@title'}
                    },
                    'attrs': {'name': 'title','edit-enable': 'true', 'origin': '@title' },
                },
            ]


motai_config = [
                {
                    'title': '组名',
                    'display': True,
                    'attrs': {'type':'input', 'class': 'form-control', 'name':'title'},
                },
            ]


search_config = [
                {'name': 'id', 'text': 'ID', 'condition_type': 'input'},
                {'name': 'title__contains', 'text': '用户组名', 'condition_type': 'input'},
            ]