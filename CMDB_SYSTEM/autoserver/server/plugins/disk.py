#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
硬盘新数据格式：
{'disk': 
    {'data': 
        {'5': 
            {'capacity': 
            '476.939', 
            'slot': '5', 
            'pd_type': 'SATA', 
            'model': 'S1AXNSAFB00549A     
            Samsung SSD 840 PRO Series              
            DXM06B0Q'}, 
            ...
'''

from repository import models


class Disk:
    def __init__(self, data, server_obj):
        self.data = data
        self.server_obj = server_obj

    @classmethod
    def initial(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def execute(self):
        new_disk_list = self.data['disk']['data']
        # 硬盘旧数据
        old_disk_list = models.Disk.objects.filter(server_obj=self.server_obj)

        # 根据槽号区分新增、修改、删除
        new_slot_list = list(self.data['disk']['data'].keys())

        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 新增
        add_list = set(new_slot_list).difference(set(old_slot_list))
        if add_list:
            self.add(new_disk_list, add_list)

        # 更新
        update_list = set(new_slot_list).intersection(set(old_slot_list))
        if update_list:
            self.update(new_disk_list, update_list)

        # 删除
        del_list = set(old_slot_list).difference(set(new_slot_list))
        if del_list:
            self.delete(del_list)

    def add(self, new_disk_list, add_list):

        record_list = []
        for slot in add_list:
            tmp = "新增硬盘:{slot} {capacity} {model} {pd_type}".format(**new_disk_list[slot])
            models.Disk.objects.create(server_obj=self.server_obj, **new_disk_list[slot])
            record_list.append(tmp)
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=";".join(record_list))

    def update(self, new_disk_list, update_list):
        map_dict = {'capacity': '容量', 'model': '型号', 'pd_type': '类型'}
        record_list = []
        for slot in update_list:
            new_disk_row = new_disk_list[slot]
            old_disk_row = models.Disk.objects.filter(server_obj=self.server_obj, slot=slot).first()
            for name, new_value in new_disk_row.items():
                old_value = getattr(old_disk_row, name)
                if old_value != new_value:
                    setattr(old_disk_row, name, new_value)
                    record_list.append("槽位%s硬盘：%s 由 %s 更变为 %s" % (slot, map_dict[name], old_value, new_value))
            old_disk_row.save()
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(record_list))

    def delete(self, del_list):
        if del_list:
            models.Disk.objects.filter(slot__in=del_list).delete()
            tmp = '硬盘移除 槽位号：%s ' % (','.join(del_list))
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=tmp)
