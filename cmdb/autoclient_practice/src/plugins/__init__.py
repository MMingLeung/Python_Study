from lib.conf.config import settings
import importlib
import traceback


class PluginsManage():
    def __init__(self, hostname=None):
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT
        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == "SSH":
            self.SSH_USER = settings.SSH_USER
            self.SSH_PWD = settings.SSH_PWD
            self.SSH_PORT = settings.SSH_PORT
            self.SSH_KEY = settings.SSH_KEY

    def execute_plugin(self):

        response = {}
        for k,v in self.plugin_dict.items():
            ret = {'status': True, 'data': None}
            try:
                method_path, cls_name = v.rsplit('.', 1)
                print(method_path)
                m = importlib.import_module(method_path)
                cls = getattr(m, cls_name)
                if hasattr(cls, "initial"):
                    obj = cls().initial()
                else:
                    obj = cls()
                result = obj.process(self.command, self.debug)
                ret['data'] = result
            except Exception as e:
                ret['status'] = False
                # AGENT basic 采集数据出错 ： ...
                ret['data'] = "[%s][%s]采集数据出错：%s" % (self.hostname if self.hostname else "AGENT", k, traceback.format_exc())
            response[k] = ret
        return response


    def command(self):
        if self.mode == 'AGENT':
            return self.__agent
        elif self.mode == 'SSH':
            return self.__ssh
        elif self.mode == 'SALT':
            return self.__salt
        else:
            raise Exception("模式不正确，必需是AGENT/SSH/SALT")


    def __agent(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self, cmd):
        salt_cmd = "salt '%s' cmd.run '%s'" %(self.hostname,cmd,)
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh(self, cmd):
        import paramiko

        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result