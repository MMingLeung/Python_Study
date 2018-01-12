from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(max_length=64, verbose_name='邮箱')
    roles = models.ManyToManyField('Role', verbose_name='拥有角色')

    def __str__(self):
        return "%s-%s" % (self.username, self.email)


class Role(models.Model):
    caption = models.CharField(max_length=32, verbose_name='角色名')
    permission = models.ManyToManyField('Permission', verbose_name='拥有权限')

    def __str__(self):
        return self.caption


class Menu(models.Model):
    caption = models.CharField(max_length=32, verbose_name='菜单名')
    parent = models.ForeignKey('self', verbose_name='父菜单', null=True, blank=True)

    def __str__(self):
        pre = ""
        parent = self.parent
        while True:
            if parent:
                pre = pre + str(self.caption)
                parent = self.parent.parent
            else:
                break
        return "%s-%s" %(pre, self.caption)


class Permission(models.Model):
    caption = models.CharField(max_length=32, verbose_name='权限名')
    url = models.CharField(max_length=32, verbose_name='URL')
    menu = models.ForeignKey('Menu', verbose_name='所属菜单', null=True, blank=True)


    def __str__(self):
        return "%s-%s" % (self.caption, self.url)

    def caption_text(self):
        return self.caption

    def caption_value(self):
        return self.caption

