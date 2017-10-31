#!/bin/bash

#for loop 30.get process id by random tag
#if got the process id, start command strace

for i in $(seq 1 30);do
    echo $i $1
    process_id=`ps -ef|grep $1 |grep -v sshpass |grep -v grep|grep -v 'session_tracker.sh' |awk '{print $2}'`
    echo "process_id: $process_id"
    if [ ! -z "$process_id" ];then
        echo '###########start run strace############'
        sudo strace -fp $process_id -t -o ssh_log/ssh_audit_$2.log;
        break;
    fi  
    sleep 1  
done;
