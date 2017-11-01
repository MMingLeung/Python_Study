from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Role(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title