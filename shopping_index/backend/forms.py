from django.forms import Form, fields, widgets
from app_shopping import models

class Commodity(Form):
    name = fields.CharField(max_length=64,
                            widget=widgets.TextInput(attrs={'class':'form-control','placeholder': '商品名称'}))
    about = fields.CharField(max_length=256,
                             widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '商品简介'}))
    price = fields.FloatField(widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '商品简介'}))
    img = fields.FileField(required=False,
        widget=widgets.FileInput(attrs={'id': "imgSelect", 'class': 'i1'}))
    p_level_id = fields.ChoiceField(
        choices=models.PriceLevel.objects.all().values_list('id', 'title'),
        widget=widgets.Select,
    )
    type_id = fields.ChoiceField(
        choices=models.Type.objects.all().values_list('id', 'name'),
        widget=widgets.Select,
    )

    def __init__(self, request, *args, **kwargs):
        super(Commodity, self).__init__(*args, **kwargs)
        self.id= request.session.get('id')
        self.request = request
        # print(type(self.id))
        # a = models.Type.objects.filter(commodity__type__id = int(self.id)).values('id', 'name')
        # print(a)
        # self.fields['p_level_id'].widget.choices = models.PriceLevel.objects.filter(commodity__p_level_id= int(self.id)).values_list('id', 'title')
        # self.fields['type_id'].widget.choices = models.Type.objects.filter(commodity__type_id= int(self.id)).values_list('id', 'name')
