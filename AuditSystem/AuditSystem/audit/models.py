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


class AuditLog(models.Model):
    '''
    审计日志
    '''


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

