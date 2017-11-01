from supermatt.service import test_v1
from app02 import models


class SuperMattXX(test_v1.BaseSupermatt):
    list_display = ['id', 'name']


test_v1.site.register(models.XX, SuperMattXX)