'''
global settings
'''

MESSAGE = '''
please input command:

# 1、send command
command: run ""your command"" --hosts ip ip ... 
such as: run ""df -h"" --hosts 192.168.3.55 10.4.3.4 or
         run ""df -h"" --hosts 127.0.0.1
         
---------------------------------------------------------

# 2、check task result
command: check_task task_id
such as: check_task 12345

---------------------------------------------------------

# 3、show all tasks
command: show tasks

# 4、exit program
command: exit
'''