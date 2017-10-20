from django.contrib import admin
from app_shopping import models
# Register your models here.
admin.site.register(models.Commodity)
admin.site.register(models.PriceLevel)
admin.site.register(models.Type)
