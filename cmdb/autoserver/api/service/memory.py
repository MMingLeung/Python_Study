from repository import models

class Memory():
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, server_info, host_name, server_obj):

    # ============处理内存===========

        if not server_info['memory']['status']:
            models.ErrorLog.objects.create(content=server_info['memory']['data'], asset_obj=server_info.asset, title='【%s】采集错误信息' % host_name)
        new_memory_dict = server_info['memory']['data']
        old_memory = models.Memory.objects.filter(server_obj=server_obj)

        new_slot_list = list(new_memory_dict.keys())
        old_slot_list = []
        for item in old_memory:
            old_slot_list.append(item.slot)
        #交集：
        update_list = set(new_slot_list).intersection(old_slot_list)

        #差集
        create_list = set(new_slot_list).difference(old_slot_list)

        #差集 老的存在新的没有
        delete_list = set(old_slot_list).difference(new_slot_list)

        #delete
        if delete_list:
            models.Memory.objects.filter(server_obj=server_obj, slot__in=delete_list).delete()
            #log
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除内存：%s" % (','.join(delete_list)), )

        #create
        record_list = []
        for slot in create_list:
            memory_dict = new_memory_dict[slot] #字典
            memory_dict['server_obj'] = server_obj
            models.Memory.objects.create(**memory_dict)
            temp = '新增内存：位置{slot},制造商{manufacturer},型号{model},容量{capacity},内存SN号{sn},速度{speed}'.format(**memory_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)

        #update
        record_list = []
        row_map = {'capacity':'容量', 'model':'型号', 'manufacturer':'制造商', 'sn':'内存SN号', 'speed':'速度'}
        for slot in update_list:
            new_memory_row = new_memory_dict[slot]
            old_memory_row = models.Memory.objects.filter(slot=slot, server_obj=server_obj).first()

            for k,v in new_memory_row.items():
                #k:capacity,slot.....
                #v:5xx,1...
                #反射
                value = getattr(old_memory_row, k)
                if v != value:
                    record_list.append("槽位%s，%s由%s变成为%s" % (slot, row_map[k], value, v))
                    setattr(old_memory_row, k, v)
            old_memory_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)
