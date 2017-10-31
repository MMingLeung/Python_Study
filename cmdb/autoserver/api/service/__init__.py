#参考agent
from autoserver import settings
import importlib
import traceback

class PluginsManage():

    def __init__(self, server_info, host_name, server_obj):
        self.server_info = server_info
        self.host_name = host_name
        self.plugin_dict = settings.PLUGINS_DICT
        self.server_obj = server_obj


    def execute_plugin(self):

        response = {}
        for k,v in self.plugin_dict.items():
            ret = {'status':True, 'data':None}
            try:
                method_path, cls_name = v.rsplit('.',1)
                m = importlib.import_module(method_path)
                cls = getattr(m, cls_name)
                if hasattr(cls, "initial"):
                    obj = cls().initial()
                else:
                    obj = cls()
                obj.process(self.server_info, self.host_name, self.server_obj)
            except Exception as e:
                ret['status'] = False
                ret['data'] = "[%s][%s]录入数据出错：%s" % (self.host_name , k, traceback.format_exc())
            response[k] = ret
        return response