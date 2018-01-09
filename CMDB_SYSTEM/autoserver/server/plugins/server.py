#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models
from django.forms.models import model_to_dict


class Server:
    def __init__(self, data, server_obj):
        self.data = data
        self.server_obj = server_obj

    @classmethod
    def initial(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def execute(self):
        new_basic_item = self.data['basic']['data']
        new_basic_list = list(self.data['basic']['data'].keys())
        old_basic_list = ['os_platform', 'os_version', 'hostname']

        # 更新
        update_list = set(new_basic_list).intersection(set(old_basic_list))
        if update_list:
            print('update')
            self.update(new_basic_item, update_list)

        # 删除
        del_list = set(old_basic_list).difference(set(new_basic_list))
        if del_list:
            print('del')
            pass
            # self.delete(del_list)

    def update(self, new_basic_item, update_list):
        map_dict = {'os_version': '系统版本', 'hostname': '主机名', 'os_platform': '系统平台',}
        record_list = []
        for item in update_list:
            old_basic_row = models.Server.objects.filter(id=self.server_obj.id).first()
            for name, new_value in new_basic_item.items():
                old_value = getattr(old_basic_row, name)
                if old_value != new_value:
                    tmp = {name:new_value}
                    setattr(old_basic_row, name, new_value)
                    models.Server.objects.filter(id=self.server_obj.id).update(**tmp)
                    record_list.append("主机%s：%s 由 %s 更变为 %s" % (item, map_dict[name], old_value, new_value))
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(record_list))

    def delete(self, del_list):
        if del_list:
            models.Server.objects.filter(hostname__in=del_list).delete()
            tmp = '内存移除 槽位号：%s ' % (','.join(del_list))
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=tmp)
