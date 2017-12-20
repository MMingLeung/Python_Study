from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Role(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

