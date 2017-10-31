from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(max_length=64)
    email = models.EmailField()
    group = models.ForeignKey("UserGroup", null=True, blank=True)
    m2m = models.ManyToManyField("Role", null=True, blank=True)

    def __str__(self):
        return self.user


class UserGroup(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name