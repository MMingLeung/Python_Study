#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models


class Cpu:
    def __init__(self, data, server_obj):
        self.data = data
        self.server_obj = server_obj

    @classmethod
    def initial(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def execute(self):
        new_cpu_item = self.data['cpu']['data']
        new_cpu_list = list(self.data['cpu']['data'].keys())
        old_cpu_list = ['cpu_model', 'cpu_physical_count', 'cpu_count']

        # 更新
        update_list = set(new_cpu_list).intersection(set(old_cpu_list))
        if update_list:
            print('update')
            self.update(new_cpu_item, update_list)

        # 删除
        del_list = set(old_cpu_list).difference(set(new_cpu_list))
        if del_list:
            print('del')
            pass
            # self.delete(del_list)

    def update(self, new_cpu_item, update_list):
        map_dict = {'cpu_model': 'CPU型号', 'cpu_physical_count': 'CPU物理核心数量', 'cpu_count': 'CPU核心数量',}
        record_list = []
        for item in update_list:
            old_cpu_row = models.Server.objects.filter(id=self.server_obj.id).first()
            for name, new_value in new_cpu_item.items():
                old_value = getattr(old_cpu_row, name)
                if old_value != new_value:
                    tmp = {name:new_value}
                    setattr(old_cpu_row, name, new_value)
                    models.Server.objects.filter(id=self.server_obj.id).update(**tmp)
                    record_list.append("主机%s：%s 由 %s 更变为 %s" % (item, map_dict[name], old_value, new_value))
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(record_list))

    def delete(self, del_list):
        if del_list:
            models.Server.objects.filter(hostname__in=del_list).delete()
            tmp = 'CPU 移除：%s ' % (','.join(del_list))
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=tmp)
