from django.db import models
from rbac.models import User as RbacUser

# Create your models here.
class UserInfo(models.Model):
    nickname = models.CharField(max_length=64)
    user = models.OneToOneField(RbacUser)
    def __str__(self):
        return self.nickname

class UserGroup(models.Model):
    title = models.CharField(max_length=64, unique=True)
    detail = models.TextField()

    def __str__(self):
        return  self.title

class UserToGroup(models.Model):
    user = models.ForeignKey(UserInfo)
    group = models.ForeignKey(UserGroup)


    class Meta:
        unique_together = [('user', 'group'),]

    def __str__(self):
        return "%s-%s" %(self.user.nickname, self.group.title)
