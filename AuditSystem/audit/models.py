from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Host(models.Model):
    '''
    主机信息
    '''
    hostname = models.CharField(verbose_name='主机名',max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(verbose_name='ip地址',unique=True)
    port = models.IntegerField(verbose_name='端口',default=22)
    idc = models.ForeignKey("IDC")

    # #主机关联多个用户
    # host_users = models.ManyToManyField('HostUser')
    #host_groups = models.ManyToManyField("HostGroup")
    enabled = models.BooleanField(verbose_name='状态',default=True)

    def __str__(self):
        return "%s-%s" %(self.hostname, self.ip_addr)


class BindHostUser(models.Model):
    host_name = models.ForeignKey('Host')
    host_user = models.ForeignKey('HostUser')

    class Meta:
        unique_together=[('host_name', 'host_user')]

    def __str__(self):
        return "%s-%s" %(self.host_name, self.host_user)


class IDC(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class HostUser(models.Model):
    '''
    远程主机的用户信息
    '''
    auth_type_choices = (
        (0,'ssh-password'),
        (1,'ssh-key'),
    )
    auth_type = models.SmallIntegerField(verbose_name='认证类型',choices=auth_type_choices)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s" % (self.auth_type, self.username, self.password)

    class Meta:
        unique_together = [
            ('username', 'password')
        ]


class HostGroup(models.Model):
    '''
    主机组
    '''
    name = models.CharField(max_length=64, unique=True)
    #只能关联BindHostUser 不能直接关联Host
    #因为关联的Host,Account通过本表又可以去获取任意的HOST
    host_user_binds = models.ManyToManyField("BindHostUser")

    def __str__(self):
        return self.name




class Account(models.Model):
    '''
    堡垒机账户
    django认证系统
    1、扩展
    2、继承
    user.account.host_user_
    '''
    #关联django自带的用户
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)

    #让用户关联主机
    host_user_binds = models.ManyToManyField("BindHostUser", blank=True)
    host_groups = models.ManyToManyField('HostGroup', blank=True)

class AuditLog(models.Model):
    '''
    审计日志
    '''
    session = models.ForeignKey("SessionLog")
    cmd = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" %(self.session, self.cmd)

class SessionLog(models.Model):
    '''
    使用堡垒机账户登录服务器一次，作为一次会话
    获取该记录id传给会话检测脚本，作为会话日志文件名
    '''
    account = models.ForeignKey("Account")
    host_user_bind = models.ForeignKey("BindHostUser")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s-%s" % (self.account, self.host_user_bind)


class Token(models.Model):

    host_user_bind = models.ForeignKey("BindHostUser")
    val = models.CharField(max_length=128,unique=True)
    account = models.ForeignKey("Account")
    expire = models.IntegerField("超时时间(s)", default=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" % (self.host_user_bind, self.val)

class Task(models.Model):
    '''
    任务表
    1、堡垒机账号account
    2、每子个任务的情况
    3、时间
    4、状态
    5、命令类型
    6、命令内容
    '''
    account = models.ForeignKey("Account")
    date = models.DateTimeField(auto_now_add=True)
    task_type_choices = ((0, 'cmd'), (1, 'file_transfer'))
    task_type = models.IntegerField(choices=task_type_choices)
    content = models.TextField("任务内容")
    timeout = models.IntegerField('任务超时', default=5)

    def __str__(self):
        return '%s-%s-%s' % (self.id, self.task_type, self.content)


class TaskLog(models.Model):
    '''
    子任务表
    1、每台主机的关系host_user_binds
    2、属于哪个task
    3、获取结果
    4、时间
    '''
    host_user_bind = models.ForeignKey('BindHostUser')
    task = models.ForeignKey('Task')
    result = models.TextField(default='init..')
    date = models.DateTimeField(auto_now_add=True)
    status_choices = ((0, 'success'), (1, 'failed'), (2, 'time_out'), (3, 'initializing'))
    status = models.IntegerField(choices=status_choices)

    class Meta:
        unique_together = ('task', 'host_user_bind')

    def __str__(self):
        return '%s-%s' % (self.id, self.host_user_bind)