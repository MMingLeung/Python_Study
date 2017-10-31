import multiprocessing
import paramiko
import os,sys
import json




def cmd_run(task_log_id, task_id, cmd_str):
    '''
    执行命令获取结果，写入数据库
    :param bind_host_obj_id: 
    :param task_id: 
    :param cmd_str: 
    :return: 
    '''
    try:
        import django
        django.setup()
        from audit import models
        task_log_obj = models.TaskLog.objects.get(id=task_log_id)
        print('run cmd:', task_log_obj, cmd_str)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(task_log_obj.host_user_bind.host_name.ip_addr,
                    task_log_obj.host_user_bind.host_name.port,
                    task_log_obj.host_user_bind.host_user.username,
                    task_log_obj.host_user_bind.host_user.password,
                    timeout=15)
        stdin, stdout, stderr = ssh.exec_command(cmd_str)

        result = stdout.read() + stderr.read()
        task_log_obj.result = result or 'cmd has no output.'
        task_log_obj.status = 0
        task_log_obj.save()
        ssh.close()
    except Exception as e:
        print("error:",e)






def file_transfer(tasklog_id, task_id, task_content):
    '''
    文件传输
    1、通过tasklog_id查询出其数据库对象，反序列化content
    2、实例化paramiko对象，连接
    3、发送：1、本地的文件、用户id、随机字符串拼接路径
            2、循环该路径内所有文件（可能有多个）
            3、sftp上传
    4、下载：1、拼接在本地下载的路径 downloads/task_id
            2、再拼接 downloads/task_id/ip/filename
            3、sftp获取
            4、
    :param tasklog_id: 
    :param task_id: 
    :param task_content: 
    :return: 
    '''
    import django
    django.setup()
    from django.conf import settings
    from audit import models
    tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)
    try:
        task_data = json.loads(tasklog_obj.task.content)
        t = paramiko.Transport((tasklog_obj.host_user_bind.host_name.ip_addr, tasklog_obj.host_user_bind.host_name.port))
        t.connect(username=tasklog_obj.host_user_bind.host_user.username, password=tasklog_obj.host_user_bind.host_user.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('begin to send or get')
        if task_data.get('file_transfer_type') == 'send':
            print('send')
            local_path = "%s/%s/%s" % (settings.FILE_UPLOADS,
                                       tasklog_obj.task.account.id,
                                       task_data.get('random_str'))
            for file_name in os.listdir(local_path):
                sftp.put("%s/%s" % (local_path, file_name), "%s/%s" % (task_data.get('remote_path'), file_name))
            tasklog_obj.result = 'send finished'
        else:
            #循环所有服务器下的目录下载
            print('get')
            download_dir = "{download_base_dir}/{task_id}".format(download_base_dir=settings.FILE_DOWNLOADS, task_id=task_id)
            if not os.path.exists(download_dir):
                os.makedirs(download_dir, exist_ok=True)
            remote_filename = os.path.basename(task_data.get('remote_path'))
            print(remote_filename)
            local_path = "%s/%s.%s" % (download_dir, tasklog_obj.host_user_bind.host_name.ip_addr, remote_filename)

            sftp.get(task_data.get('remote_path'), local_path)

            tasklog_obj.result = 'get remote file [%s] to local done ' % (task_data.get('remote_path'))
            print('111111')
        t.close()
        tasklog_obj.status = 0
        tasklog_obj.save()

    except Exception as e:
        print('error:', e)
        tasklog_obj.result = str(e)
        tasklog_obj.save()


if __name__ == '__main__':
    # 需要调用django的models,必需把django程序顶层目录路径加入系统变量
    # 还需要配置django,注册app
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuditSystem.settings")
    import django
    django.setup() #手动注册django所有APP
    from audit import models

    # 获取任务id，从而获取任务对象
    print('begin to get task id')
    # 获取参数
    task_id = int(sys.argv[1])
    print('task_id', type(task_id), task_id)
    task_obj = models.Task.objects.get(id=task_id)
    print(task_obj)
    # 调用多进程
    pool = multiprocessing.Pool(processes=10)

    # 判断任务类型（cmd/file_translate）
    print('begin to run: cmd_run')
    if task_obj.task_type == 0: #cmd
        task_func = cmd_run
    else:
        task_func = file_transfer
    for tasklog_obj in task_obj.tasklog_set.all():
        pool.apply_async(task_func, args=(tasklog_obj.id, task_obj.id, task_obj.content))
    pool.close()
    pool.join()

