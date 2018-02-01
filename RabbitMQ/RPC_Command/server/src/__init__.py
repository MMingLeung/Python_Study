#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
The main program logic
'''
import re
from concurrent.futures import ThreadPoolExecutor
from server.config.conf import settings
from server.src.my_rpc import MyRPCCommand

pool = ThreadPoolExecutor(20)
results = []
rpc_connection_list = []

def start():
    while True:
        print(settings.MESSAGE)
        user_input = input(">>: ")
        if not user_input:
            continue

        if re.match('check_task .*', user_input):
            for result in results:
                if result['task_id'] == user_input.split(' ')[1]:
                    print('task_id: {task_id}\n'
                          'result: {content} '.format(
                        task_id=result['task_id'],
                        content=result['content'],
                    ))
        elif re.match('run "".*"" --hosts .*', user_input):
            command = re.findall('""(.*)""', user_input)
            ip_list = re.findall('\d+\.\d+\.\d+\.\d+', user_input)
            publish_cmd = command[0]
            for ip in ip_list:
                if not rpc_connection_list:
                    command_obj = MyRPCCommand(ip)
                    tmp = pool.submit(command_obj.call, publish_cmd)
                    results.append(tmp.result())
                    temp = {'ip': ip, 'con': command_obj}
                    rpc_connection_list.append(temp)
                else:
                    for rpc_dict in rpc_connection_list:
                        if ip not in rpc_dict['ip']:
                            command_obj = MyRPCCommand(ip)
                            tmp = pool.submit(command_obj.call, publish_cmd)
                            results.append(tmp.result())
                            temp = {'ip': ip, 'con': command_obj}
                            rpc_connection_list.append(temp)
                        else:
                            command_obj =rpc_dict['con']
                            tmp = pool.submit(command_obj.call, publish_cmd)
                            results.append(tmp.result())

            for result in results:
                print('task_id: {task_id}\n'
                      'cmd: {command}\n'
                      '----------------------'.format(
                    task_id=result['task_id'],
                    command=result['command'],
                ))
        elif re.match('show tasks', user_input):
            for result in results:
                print('task_id: {task_id}\n'
                      'cmd: {command}\n'
                      '-----------------------'.format(
                    task_id=result['task_id'],
                    command=result['command'],
                ))
        elif re.match('exit', user_input):
            for rpc_dict in rpc_connection_list:
                rpc_dict['con'].channel.close()
                print('%s connection close successed!' % rpc_dict['ip'])
            print('see you!')
            exit()
