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
             'attrs': {'k1': 'v1', 'k2': '@id'},
             },

            {'q': 'device_type_id', 'title': '资产类型', 'display': True, 'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@@device_type_choices'}
            },
             'attrs': {'global-key':'device_type_choices','edit-type':'select','edit-enable': 'true', 'origin': '@device_type_id', 'name':'device_type_id'},
             },

            {'q': 'device_status_id', 'title': '资产状态', 'display': True, 'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@@device_status_choices'}
            },
             'attrs': {'global-key':'device_status_choices','edit-type':'select','edit-enable': 'true', 'origin': '@device_status_id','name':'device_status_id'},
             },

            {'q': 'cabinet_num', 'title': '机柜号', 'display': True, 'text': {
                'tpl': 'BJ-{n1}',
                'kwargs': {'n1': '@cabinet_num'}
            },
             'attrs': {'edit-enable': 'true','origin':'@cabinet_num', 'name':'cabinet_num'},
             },

            {'q': 'idc__name', 'title': '机房', 'display': True, 'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@idc__name'}
            },
             'attrs': {'global-key':'idc_choices','edit-type':'select','edit-enable': 'true', 'k2': '@idc__name','origin':'@idc_id','name':'idc_id'},
             },

            {'q': 'idc_id',
             'title': '',
             'display': False,
             'text': {},
             'attrs': {},
             },

            # 页面显示：  标题：操作    删除、编辑（a标签）
            {'q': None, 'title': '操作', 'display': True, 'text': {
                'tpl': '<a href="/del?nid={n1}">删除</a>',
                'kwargs': {'n1': '@id'}
            }
             },
        ]

search_config = [

            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_choices'},
            #模糊匹配
            {'name': 'cabinet_num__contains', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select',
             'global_name': 'device_status_choices'},
        ]