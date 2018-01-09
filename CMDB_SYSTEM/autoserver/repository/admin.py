from django.contrib import admin
from .models import Disk, AssetRecord, ErrorLog, IDC, Asset

# Register your models here.
admin.site.register(Disk)
admin.site.register(AssetRecord)
admin.site.register(ErrorLog)
admin.site.register(IDC)
admin.site.register(Asset)