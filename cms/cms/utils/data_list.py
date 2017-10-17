from django.db.models import Q
import json


def get_data_list(request, table_config, model_cls):
    '''
    获取前端发送的GET请求，获取查询条件condition，查询数据
    :param request: 
    :return: 
    '''
    condition = request.GET.get('condition')
    condition_dict = json.loads(condition)

    con = Q()
    for name, values in condition_dict.items():
        ele = Q()  # select * from where xx=1 or xx=2
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name, item))
        con.add(ele, 'AND')

    values_list = []
    # 把‘q’添加到列表中，作为数据库查询的条件
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])
    data = model_cls.objects.filter(con).values(*values_list).order_by('id')
    return data