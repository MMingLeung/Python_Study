from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=64, verbose_name='用户名')
    email = models.CharField(max_length=64, verbose_name='邮箱')
    ug = models.ForeignKey('UserGroup', blank=True, null=True, verbose_name='用户组')
    ur = models.ManyToManyField('Role', blank=True, null=True, verbose_name='角色')

    def text_username(self):
        return self.username

    def value_username(self):
        return self.username

    def text_email(self):
        return self.email

    def value_email(self):
        return self.email

    def __str__(self):
        return '%s-%s' % (self.username, self.email)

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class Role(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title