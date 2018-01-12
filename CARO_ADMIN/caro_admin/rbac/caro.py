from rbac.models import Permission
from caroadmin import service
from django.urls import reverse
from django.utils.safestring import mark_safe
from caroadmin.utils.filter import FilterOption


class PermissionAdmin(service.BaseCaro):

    def operate(self, obj=None,is_header=None):
        if is_header:
            return '操作'
        else:
            base_change_url = reverse("{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(base_change_url, self.request.GET.urlencode())
            change_tpl = "<a href={}>编辑</a>".format(change_url)
            return  mark_safe(change_tpl)

    list_display = ['id', 'caption', 'url', 'menu_id', operate]

    filter_list = [
        FilterOption('caption', is_multi=False, text_func='caption_text', value_func='caption_value'),
    ]

service.site.reigster(Permission, PermissionAdmin)