import json
from threading import Thread
from django.db.transaction import atomic
from audit import models
import subprocess
from AuditSystem import settings


class Task:
    def __init__(self, request):
        '''
        初始化
        :param request: 
        '''
        self.request = request
        self.error = []
        self.task_data = None


    def is_valid(self):
        '''
        判断命令和主机列表是否合法
        :return: 
        '''
        task_data = self.request.POST.get('task_data')
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get('task_type') == 'cmd':
                if self.task_data.get('cmd') and self.task_data.get('selectd_hosts_ids'):
                    return True
                self.error.append({'invalid_argument':'cmd or host_ids not exits'})
            elif self.task_data.get('task_type') == 'file_transfer':
                return True
            else:
                self.error.append({'invalid_argument': 'task_type is not exits'})
        self.error.append({'invalid_argument': 'task_type is not exits'})


    def run(self):
        task_func = getattr(self, self.task_data.get('task_type'))
        task_obj = task_func()
        return task_obj


    def cmd(self):
        '''
        1、生成任务id（Task表创建数据）
        2、准备ip列表（去重）
        3、生成子任务记录（TaskLog表创建数据）
        4、启动独立进程，在其中运行多线程
        :return: 
        '''

        task_obj = models.Task.objects.create(task_type=0,
                                              account=self.request.user.account,
                                              content=self.task_data.get('cmd')
                                              )
        print('finish create task :',task_obj)
        task_log_objs = []
        host_ids = set(self.task_data.get('selectd_hosts_ids'))
        for host in host_ids:
            task_log_objs.append(
                models.TaskLog(task_id=task_obj.id, host_user_bind_id=host, status=3))
        models.TaskLog.objects.bulk_create(task_log_objs, 100)



        multi_task = subprocess.Popen("python3.5 %s %s" % (settings.MULTI_TASK_DIR, task_obj.id),
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        print("task result:", multi_task.stdout.read(), multi_task.stderr.read().decode('utf8'))
        return task_obj,multi_task



    def file_transfer(self):
        '''
         文件上传
         file_transfer_type
         random_str
         remote_path
        :return: 
        '''
        task_obj = models.Task.objects.create(task_type=1,
                                              account=self.request.user.account,
                                              content=json.dumps(self.task_data)
                                              )
        print('finish create task :', task_obj)
        task_log_objs = []
        host_ids = set(self.task_data.get('selectd_hosts_ids'))
        for host in host_ids:
            task_log_objs.append(
                models.TaskLog(task_id=task_obj.id, host_user_bind_id=host, status=3))
        models.TaskLog.objects.bulk_create(task_log_objs, 100)

        multi_task = subprocess.Popen("python3.5 %s %s" % (settings.MULTI_TASK_DIR, task_obj.id),
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        print("task result:", multi_task.stdout.read(), multi_task.stderr.read().decode('utf8'))
        return task_obj,multi_task
