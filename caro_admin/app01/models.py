#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
项目管理系统数据库
'''
from django.db import models
from rbac.models import User


class WorkSpace(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def work_space_value(self):
        return self.pk

    def work_space_text(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='部门名称')
    description = models.TextField('部门情况描述')
    floor = models.IntegerField('部门所在楼层')

    def __str__(self):
        return self.name


class ProjectList(models.Model):
    work_space = models.ForeignKey('WorkSpace', verbose_name='办公区')
    department = models.ForeignKey('Department', verbose_name='部门')
    type_choice = ((0, '新建项目'), (1, '维护'), (2, '改造'))
    class_type = models.SmallIntegerField(choices=type_choice, default=0)
    status_choice = ((0, '未完成'), (1, '完成'), (2, '在建'))
    status_type = models.SmallIntegerField(choices=status_choice, default=0)
    duration = models.IntegerField('工期')
    price = models.FloatField('费用', default=0)
    start_data = models.DateField('项目开始日期')
    end_data = models.DateField('项目结束日期', blank=True, null=True)

    staff = models.ManyToManyField('UserProfile', verbose_name='负责人员')

    def __str__(self):
        return "%s-%s" % (self.department, self.class_type)


class UserProfile(models.Model):
    user_obj = models.OneToOneField('rbac.User')
    name = models.CharField(max_length=32)
    workspace = models.ForeignKey('WorkSpace', verbose_name='所属办公区', blank=True, null=True)
    memo = models.TextField('备注', blank=True, null=True, default=None)
    data_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectRecord(models.Model):
    project = models.ForeignKey('ProjectList', verbose_name='项目')
    day_num = models.IntegerField("节次", help_text='添加项目进行到第几天')
    date = models.DateField(auto_now_add=True, verbose_name='开始工程日期')
    engineer = models.ForeignKey('UserProfile', verbose_name='项目工程师')
    project_detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s 第%s天" % (self.project, self.day_num)

    class Meta:
        unique_together = ('project', 'day_num')


class Reporter(models.Model):
    phone = models.CharField(max_length=64, unique=True, help_text='项目/报修人电话号码')
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name='项目/报修人')
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField(choices=sex_type, default='male', max_length=32)
    department = models.ForeignKey('Department', blank=True, null=True)
    notes = models.TextField(verbose_name='项目/报修者联系记录')

    def __str__(self):
        return '%s-%s' % (self.name, self.department)


class ReporterFollowerUp(models.Model):
    reporter = models.ForeignKey('Reporter', verbose_name='项目/报修者')
    note = models.TextField('跟进内容')
    status_choices = (
        (1,'项目/维护未完成'),
        (2,'项目/维护1周完成'),
        (3,'项目/维护2周完成'),
        (4,'项目/维护1个月完成'),
        (5,'项目/维护2个月完成'),
        (6,'项目/维护3个月完成'),
        (7,'项目/维护3个月以上完成'),
    )
    status = models.IntegerField(choices=status_choices, help_text='项目/维修此时的状态')
    consultant = models.ForeignKey('UserProfile', verbose_name='跟踪人')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" % (self.reporter, self.status)



