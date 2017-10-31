from repository import models
from django.forms import Form, fields, widgets

class AssetForm(Form):

    device_type_id = fields.IntegerField(
        widget=widgets.Select(choices=models.Asset.device_type_choices, attrs={'class': 'form-control'}))
    device_status_id = fields.IntegerField(
        widget = widgets.Select(choices=models.Asset.device_status_choices, attrs={'class': 'form-control'}))
    cabinet_num = fields.CharField(max_length=30,
            widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '机柜号'})
                        )
    cabinet_order = fields.CharField(max_length=30,
            widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '机柜内序号'})
                        )
    idc = fields.ChoiceField(
        choices=models.IDC.objects.values_list("id", "name"),
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    business_unit = fields.ChoiceField(
        choices=models.BusinessUnit.objects.values_list("id", "name"),
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    tag = fields.MultipleChoiceField(
        choices=models.Tag.objects.values_list("id", "name"),
        widget=widgets.CheckboxSelectMultiple(attrs={'class': 'form-control'})
    )
    latest_date = fields.DateTimeField()