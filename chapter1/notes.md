# 一、常用命令

1. su - root    切换用户
1. init 0 关机 6 重启
1. shutdown -h now
1. who 查看登录的用户
1. tty 查看登录的终端
1. date 月日时分年
1. ctrl + alt + 2  切换文本模式
1. cal M Y   查看日历
1. passwd 修改密码
1. echo 123 | passwd --stdin root  通过管道传密码给passwd   
1. man + 命令 查看说明
1. mkdir 新建文件夹
1. move 更改文件名
1. rm -r 递归删除 -f 强制
1. less more 
1. head -n 1 查看第一行或默认10行
1. tail -n 同上 -f 动态查看
1. echo XXXX >> a.txt 把XXXXX写入文件
1. histroy
find / -type f -name XXX -size +XXM  普通文件是f 找出>XXM 的文件
1. ls -ld    查看目录详细信息
1. mkdir /a/v/c/s/ -p 建立文件夹
