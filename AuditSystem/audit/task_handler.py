class Task(object):
    '''
    批量处理用户发送的命令
    '''
    def __init__(self, request):
        self.request = request
