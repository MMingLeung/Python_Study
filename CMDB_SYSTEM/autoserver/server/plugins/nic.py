#!/usr/bin/env python
# -*- coding:utf-8 -*-
from repository import models


class Nic:
    def __init__(self, data, server_obj):
        self.data = data
        self.server_obj = server_obj

    @classmethod
    def initial(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def execute(self):
        new_mem_list = self.data['nic']['data']
        for key, value in new_mem_list.items():
            value['name'] = key
        old_mem_list = models.NIC.objects.filter(server_obj=self.server_obj)

        # 根据槽号区分新增、修改、删除
        new_slot_list = list(self.data['nic']['data'].keys())

        old_slot_list = []
        for item in old_mem_list:
            old_slot_list.append(item.name)

        # 新增
        add_list = set(new_slot_list).difference(set(old_slot_list))
        if add_list:
            self.add(new_mem_list, add_list)

        # 更新
        update_list = set(new_slot_list).intersection(set(old_slot_list))
        if update_list:
            self.update(new_mem_list, update_list)

        # 删除
        del_list = set(old_slot_list).difference(set(new_slot_list))
        if del_list:
            self.delete(del_list)

    def add(self, new_mem_list, add_list):
        record_list = []
        print(new_mem_list)
        print(add_list)
        for slot in add_list:
            tmp = "新增网卡:{hwaddr} {netmask} {ipaddrs} {up} ".format(**new_mem_list[slot])
            models.NIC.objects.create(server_obj=self.server_obj, **new_mem_list[slot])
            record_list.append(tmp)
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=";".join(record_list))

    def update(self, new_mem_list, update_list):
        map_dict = {'name': '名称', 'hwaddr': 'mac地址', 'netmask': '子网掩码', 'ipaddrs':'IP地址', 'up':'启动'}
        record_list = []
        for slot in update_list:
            new_nic_row = new_mem_list[slot]
            old_nic_row = models.NIC.objects.filter(server_obj=self.server_obj, name=slot).first()
            for name, new_value in new_nic_row.items():
                old_value = getattr(old_nic_row, name)
                if old_value != new_value:
                    setattr(old_nic_row, name, new_value)
                    record_list.append("网卡%s：%s 由 %s 更变为 %s" % (slot, map_dict[name], old_value, new_value))
            old_nic_row.save()
        if record_list:
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(record_list))

    def delete(self, del_list):
        if del_list:
            models.NIC.objects.filter(name__in=del_list).delete()
            tmp = '内存移除 槽位号：%s ' % (','.join(del_list))
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=tmp)
