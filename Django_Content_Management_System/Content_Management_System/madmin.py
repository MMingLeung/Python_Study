from mattadmin import service
from Content_Management_System import models

class MyBaseMatt(service.BaseSupermatt):

    def initial(self, request):
        pk_list = request.POST.getlist('pk')
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='init')
        return True

    initial.text = '初始化'

    action_list = [initial, ]

    list_display = ['id','username','email']


service.site.register(models.UserInfo, MyBaseMatt)