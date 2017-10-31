from repository import models

class Disk():
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, server_info, host_name, server_obj):

    # ============处理硬盘（上课内容）===========

        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(content=server_info['disk']['data'], asset_obj=server_info.asset, title='【%s】采集错误信息' % host_name)
        new_disk_dict = server_info['disk']['data']
        old_disk = models.Disk.objects.filter(server_obj=server_obj)

        new_slot_list = list(new_disk_dict.keys())
        old_slot_list = []
        for item in old_disk:
            old_slot_list.append(item.slot)
        #交集：
        update_list = set(new_slot_list).intersection(old_slot_list)

        #差集
        create_list = set(new_slot_list).difference(old_slot_list)

        #差集 老的存在新的没有
        delete_list = set(old_slot_list).difference(new_slot_list)

        #delete
        if delete_list:
            models.Disk.objects.filter(server_obj=server_obj, slot__in=delete_list).delete()
            #log
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除硬盘：%s" % (','.join(delete_list)), )

        #create
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot] #字典
            disk_dict['server_obj'] = server_obj
            models.Disk.objects.create(**disk_dict)
            temp = '新增硬盘：位置{slot},容量{capacity},型号{model},类型{pd_type}'.format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)

        #update
        record_list = []
        row_map = {'capacity':'容量', 'pd_type':'类型', 'model':'型号'}
        for slot in update_list:
            new_disk_row = new_disk_dict[slot]
            old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()

            for k,v in new_disk_row.items():
                #k:capacity,slot.....
                #v:5xx,1...
                #反射
                value = getattr(old_disk_row, k)
                if v != value:
                    record_list.append("槽位%s，%s由%s变成为%s" % (slot, row_map[k], value, v))
                    setattr(old_disk_row, k, v)
            old_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)
