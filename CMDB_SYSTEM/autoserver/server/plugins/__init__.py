'''
插件介绍：
    本插件的作用是对各个硬件的信息进行新旧对比并且入库。
    
    增加插件方式：
        在/autoserver/settings.py文件中,API_PLUGINS配置按格式增加即可。
        API_PLUGINS = {
            'Disk':'server.plugins.disk.Disk',
            'Memory':'server.plugins.memory.Memory',
            'Nic':'server.plugins.nic.Nic',
            'Server':'server.plugins.server.Server',
            'Cpu':'server.plugins.cpu.Cpu',
            }
'''