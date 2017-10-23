from django.contrib import admin
from audit import models
# Register your models here.
admin.site.register(models.HostGroup)
admin.site.register(models.Host)
admin.site.register(models.HostUser)
admin.site.register(models.BindHostUser)
admin.site.register(models.Account)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)