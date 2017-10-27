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

            {'q': 'name', 'title': '机房名称', 'display': True, 'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@name'}
            },
             'attrs': {'edit-enable': 'true','origin': '@name', 'name': 'name'},
             },

            {'q': 'floor', 'title': '楼层', 'display': True, 'text': {
                'tpl': '{n1}',
                'kwargs': {'n1': '@floor'}
            },
             'attrs': {'edit-enable': 'true', 'origin': '@floor', 'name': 'floor'},
             },

            # 页面显示：  标题：操作    删除、编辑（a标签）
            {'q': None, 'title': '操作', 'display': True, 'text': {
                'tpl': '<a href="/del?nid={n1}">删除</a>',
                'kwargs': {'n1': '@id'}
            }
             },
        ]