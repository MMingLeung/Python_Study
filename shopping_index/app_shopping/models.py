from django.db import models

# Create your models here.
class Commodity(models.Model):
    name = models.CharField(max_length=64, verbose_name='商品名称', unique=True)
    about = models.CharField(max_length=256)
    price = models.FloatField()
    img = models.ImageField()
    p_level = models.ForeignKey(to='PriceLevel', verbose_name='价格等级', to_field='id' ,null=True, blank=True)
    type = models.ForeignKey(to='Type', verbose_name='商品类型', to_field='id' ,null=True, blank=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=32)


    def __str__(self):
        return "%s" % (self.name )


class PriceLevel(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return "%s" % (self.title)