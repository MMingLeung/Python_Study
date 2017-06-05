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

# 二、权限管理
1. useradd + name新建用户

   id + 用户名 查询改用户信息
1. /etc/passwd 用户信息

    /etc/shadow 用户密码
      
    /etc/group   组信息
      
    userdel 用户名 删除用户
    gpasswd 用户名  修改用户组密码
    usermod -G 组名 用户名
 
* 可以用在/etc下passwd shadow group添加用户 ，在skel添加隐藏文件
 
 
drwxr-xr-x. 6 root root 57 5月  12 13:05 /home/
                      
                              
              属主  属组

修改权限 chmod (r=4 w=2 x=1)或chmod u=/+ , g=/+ , o=/+
* 对于目录 r 读取名录里面的文件名  x 能够进入目录或删除

(1)对于文件
read: 能看内容
write:修改内容
x:执行文件

(2)对于目录
read:浏览目录下的子目录名，子文件名
write:创建修改文件名，子文件名。但是不能改内容
x:可以用cd进入目录

# 三、打包
1. tar -cf 目标文件名 要压缩的文件      ---  打包
             
    c= create f=filename
      
    tar -xfv 文件名  ---解包

1. gzip 压缩  gunzip解压缩(压缩快但压缩程度高低）

   tar -cvzf XXX.tar.gz   打包加压缩

2. bzip2 压缩（压缩慢但压缩程度高）   
    
    tar -cvjf  XXX.tar.bz2
             -j:bzip2压缩        
1. tar -xf xxx.tar.gz -C /XXX/解压缩
                   -C：change to directory DIR

# 四、磁盘分区
1、/dev/sda   s:scsi     d:disk      a:第一块硬盘

2、查看分区  df -h -T

3、磁盘分区命令
fdisk -l /dev/sd?   查看磁盘分区
fdisk /dev/sd?

逻辑分区：扩展分区的分区

4、makefilesystem
     mkfs格式化
    .ext4   .xfs

5、mount /dev/db? /XXX   XXX目录挂载到/db?分区下
     umount /dev/sdb? -l（强制卸载）

6、touch /XX/{1..1000XX}.txt     建立1000XX个TXT

7、du -sh /XX 统计文件夹内文件大小

8、ll -di 查看目录的innode号

删除
（1）先把innode编号变成free 
（2）再把文件与自身innode编号关系解除
（3）block变成游荡，但是数据还有
     
9、软连接（快捷方式）
ln -s /XXX.xxx /XXX.xxx
     /要建立软连接的文件    /软连接名称

          

10、硬链接 ln 无法跨分区
共享一个innode号

11、VIM
:%s /xxx/xxx/g 全部替换
 

# 五、进程管理
1、swapon -s 查看swap分区
     mkswap /dev/sdbX 格式化swap
     swapon -a /dev/sdbX  挂载
     swapoff /dev/sdbX 停用

     
2、free 看内存

3、buff  还没有写进硬盘的
     cache 缓存，已经读到的东西
 
4、清理缓存 
     echo 3 > /proc/sys/vm/drop_caches

5、进程管理
     查看ps aux
     ps aux |grep gnome
                   过滤

4、 结束进程 kill -9 PID
                    pkill -9 软件名

                    jobs查看工作号 然后 kill -9 %1

5、后台进程 软件名 + &

6、pstree 进程树

7、pgrep + 软件名    #只显示软件pid

8、dd if=/dev/zero of=/b.txt bs=1G count=1
测试硬盘速度 从zero取出数据写到b.txt 1个1G 的文件

9、软件包管理
（1）二进制 
rpm -ivh  --force 强制覆盖   
#   i:install  v:views h:进度条
rpm -qi XXX软件名     查看软件信息
rpm -qa | XXXX   查看是否有该软件

rpm -ql XXXX   查看软件位置

rpm -qf /XXX/XXX/xxx 查看该文件是哪个文件包

which ls  查看ls 的文件位置

rpm -e XXX软件名   删除软件 
     
rpm -e ` rpm -qa | grep XXX 删除软件
解决依赖性-----yum /packeages/
yum clean all 清楚缓存
yum -y install XXX 软件包名（不用写全）
yum -y erase  XXX 删除软件
     

yum install epel-* -y  
yum makecache -y 建立缓存，提高安装速度
yum update -y 升级系统
yum reinstall XX 重新安装
yum upgrade 更新软件包不更新内核
/etc/yum/yum-cron.conf 修改download_updates = no 设置不更新



createrepo 建立依赖性

yum---->repodata----->createrepo
[name]
name=aaaaa
baseurl=http://XXXX/
enabled=1
gpgcheck=0

（2）源码包
1、XSHELL远程连接

2、gcc glibc 安装gcc编译二进制代码
          yum grouplist  安装软件包组合
          yum groupinstall  '开发工具' -y    

3、安装python 
       (1) 下载pyhton.gz 
       (2)cd python 
       (3)./configuration --prefix=/usr/local/python2.7  把python 安装到该目录
       (4)make && make install
       (5)添加环境变量PATH= /usr/local/python2.7/bin:$PATH -->>   vim /etc/profile
       (6)echo $PATH

# 六、网络服务
1、top 实时刷新

2、vmstat 显示内存信息

3、netstat -tunaple 看网络连接情况

4、nginx web软件
     （1）先装扩展包yum install epel-release -y
     （2）安装 yum -y install nginx
     （3）systemctl start nginx
     （4）iptables -F 清防火墙 or  systemctl stop firewalld        (disable开机也不开启防火墙 )
     （5）就可以发送请求
     （6）systemctl reload nginx 重新读取配置

     配置文件位置：/etc/nginx/nginx.conf 
                         日志位置：/var/log/nginx/access.log
     （7）反向代理
               

5、nagios 监控软件

# 七、NFS
1、yum install -y prcbind nfs-utils 

exportfs -avr   #重新读取exportfs

-a exports all directory
-r  reexports


2、/etc/exports
共享配置/share XXX.XXX.XXX.XXX(rw,sync,fsid=0)
     文件夹名字                            读写，同步，

对other 开启r 权限
chmod  -R o+rw /share
         
3、配置ip
临时修改：ifconfig 网卡名 XXX.XXX.XXX.XXX

4、启动服务
设置开始启动：
systemctl enable nfs-server.service
systemctl enable   rpcbind.service
systemctl  start rpcbind.service
systemctl  start nfs-server.service

systemctl status XXXX 查看启动状态

/exportfs 查看那个文件共享了

showmount -e 共享列表
                    -a 多少个挂载到共享存储

(2).其他主机输入
showmount -e XXX.XXX.XXX.XXX 服务器的ip
mount -t nfs XXX.XXX.XX.XXX:/share /var/www/html
        指定文件类型

# 八、网络配置
1、ifconfig 

2、设置DNS
     nameserver XXX.XXX.XXX.XXX
     网关
     route add default gw 192.168.1.254 netmask 255.255.255.0
     route -n 查看
     ————————
     永久修改
3、cd /etc/sysconf/network-scripts

     vim ifcfg-XXXX 
     bootproto='static'
     IPADDR='XXX.XXX,XXX,XXX'
     NETMASK='255.255.255.0'
     GATEWAY='XXX.XXX.XXX.XXX'
     DNS1='192.168.X.254'

4、vim /etc/hosts
 
hostnamectl set-hostname XXXX

5、查看本机端口
netstat -an |grep 22

scp -r 本地路径  服务端ip:/tmp 上传
scp -r 服务端ip:/tmp 本地路径 下载

ssh: 
ssh-keygen 建立秘钥
ls /root/.ssh   id_rsa 钥匙  id_ras.pub锁---》发给服务端
ssh-copy-id -i 服务器ip     ——————》/root/.ssh/authorized_keys

配置文件/etc/ssh/sshd_config 重启服务 systemctl restart sshd
————————————————————————————————
修改port 端口
ssh XXXX -p XX 
或者再次生成
ssh-keygen
ssh-copy -i id_rsa.pub XXX -pXX


nfs:
安装：yum install rpcbind nfs-utils -y

配置：vim /etc/exports
/XXX XXX.XXX.XXX.0/24(rw,sync,fsid=0)
chmod -R o+w /XXX

启动：
systemctl enable nfs-server.service
          
systemctl enable rpcbind.service
          
systemctl start nfs-server.service
          
systemctl start rpcbind.service

确认：systemctl status ...
 
 exportfs

# 九、SHELL
1、source 执行 .sh文件

2、a.sh       chmod o+x 
    
    function test() {
    read -p 'please input your name:' name;
    hostnamectl set-hostname name;
    hostname;
    }


# 十、脚本
1、登录自动加载顺序
    1 /etc/profile       #Python PATH写在这里
    2 /etc/profile.d     
    3 /root/bash_profile
    4 /root/.bashrc
    5 /etc/bashrc    #添加全局变量
 
/etc/.bashrc echo '/etc/.bashrc'    
/root/.bashrc echo '/etc/.bashrc'

      /etc/.bash_profile echo '/etc/.bash_profile'
     /root/.bashrc echo '/.bash_bashrc'

     /etc/profile.d   echo '/etc/profile.d/a.sh'       chmod o+x

2、正则表达式及grep、sed、awk

grep '正则表达式' /文件路径 ————找到匹配的行
-n 显示行数
-o 只显示匹配内容
-q 静默模式 echo $? 显示为0则匹配到内容
-l 执行成功，显示文件名
-A x匹配内容后x行也打印出来
-B  X前X行
-C X上下X行
-c 匹配内容数目
-E =egrep
-i 忽略大小写
-v 取反
-r 递归目录

（1）^ --- 以....开头
（2）$ --- 以...结尾
（3）.   --- 任意一个字符
（4）*   ---左边字符任意0 ---无数个字符   
（5）+ ---- 要用-E ，左边字符有一个或无数个
（6）{N} ----出现 N次
（7）{N,M} ----出现N-M次
（8）？ ----左边字符出现0次或1次
（9）[ ] ----匹配里面的一个
（10）（XX|XXX）XX或者XXX匹配
touch {1..3}{1..c}.txt

3、SED 流编辑器

sed -n ' ' XXX.XX

-n 静默
-e 多个规则
-i 处理完写入文件
-f 规则写入文件

引号里面内容： '3a XXX'  追加一行 XXX
                        '3d' 删除第三行
                        '3p' 打印第三行
                        '3c XXX' 替换第三行为XXX 
                        '3i XX' 第三行前加一行 XX

正则定位：
               '/^root/d'  root 开头一行删除
               '1d;3d' 删除第一第三行
               '1,3d' 删除1~3行
               '4s/aaa/bbb/g'  把aaa换成bbb g:全替换  4:行数
                '/^[0-9][a-Z]+$/s/aaa/bbb/g'  整行描述，把aaa全部换成bbb
               sed -r '/^[0-9]([a-Z]{3})xsb$/ s/aaa/bbb/g'

               sed -r 's/^([a-Z]+)([^a-Z])/ \1\2/g'
                                                       \1:第一部分 \2:第二部分

巧用>> 追加备份

4、awk （有规律的）
awk -F: ' NR==1 {print $1,$2,"-----------",NF,}' /etc/passwd    
取分隔符第一列 第二列内容   NF： 段的数目     NR：行号（可以用==,>,<）
制定分隔符：   $1第一列

awk -F: '/nologin$/ {print $1}' /etc/passwd 打印以nologin 结尾的第一列

awk -F:'$1~/^r.*t$/{print $3}' /etc/passwd
          针对第一列
            $1=='root' {}  如果$1等于root 则执行{}里面内容

       -v x=$var 取变量的值 '{print x}'

5、常用命令
sort 排序 | uniq 去重 -c看了去了多少行echo

cut -d: -f1
  以： 切分   取第（N）部分
6、shell script

cp -r /etc/skel/.[!.]* /tmp 把skel目录下. 开头后面接非点的字母文件拷贝


（1）命名
清晰、字母或者下划线开头
文件名要加上扩展名
nev 查看系统变量

赋值name=aaa
显示echo $name
取消unset name

export XXX=XXX 全局变量 
（2）运算符
[ 2 > 1 ]...


（3）expr 计算器
expr 1+2 
3

yum install bc -y 

安装bc包运行浮点运算

echo 'scale=2;30/1000' | bc -l
              保留两位小时

计算运行内存占的比例

    men_tol=`free | awk 'NR==2 {print $2}'`
    men_tol=`free | awk 'NR==2 {print $3}'`
    echo "scale=2;$men_used/$men_tol" | bc -l | cut -d. -f2


（4）测试文件状态

[root@localhost ~]# test -d /etc/      -d:是否目录

[root@localhost ~]# echo $?
0


-e 是否文件
-f 是否存在和标准文件
-h 是否存在和是否链接文件
-rwx 是否有读写执行权限

（5）、脚本

    #!/bin/bash   指定用哪个命令解释器解释

    var='/etc/passwd'
    if [ -f $var ]
        then
            echo "$var is regular file"
    elif [ -b $var ]
        then
            echo "$var is deirectory file"
    elif [ -d $var ]
        then
            echo "$var is block file"
    else
        echo "$var is unknow file"
    fi

    #!/bin/bash
    echo $1      $1：接收的第一个参数            read -p 'please input:' var
    if [ -f $1 ]
        then
            echo "$1 is regular file"
    elif [ -b $1 ]
        then
            echo "$1 is deirectory file"
    elif [ -d $1 ]
        then
            echo "$1 is block file"
    else
        echo "$1 is unknow file"
    fi

输入： ./test.sh /etc/passwd

cp test.sh /etc/bin 就可以直接 test.sh /XXX 直接使用，或者加入/etc/profile内


$0:文件名

$1-{10}:

$$: pid

$*:全部参数

$@:全部参数

$#:总数

$?:上一条命令执行成功没有 0，1？

循环结构
while  [   ]
do
    echo '   '
    break
done 

echo -e "qweqwe\nwqeqwe" -e 之后\n是换行符

登录脚本：

    #!/bin/bash
    while :
    do
        read -p 'please input your name :' name
        read -p 'please input your password :'  password
        if [ -z $name ] || [ -z $password  ]
           then
                  continue
        fi
    
        if [ $name = 'Matt' ] && [ $password = '123456' ]
            then
                echo 'login successful'
                while :
                do
                   read -p 'please input your cmd :' cmd
                   if [ $cmd = 'quit' ]
                      then
                          break
                   fi
                   $cmd
                done
         else
            echo "username of password is error"
         fi
    done
    
    echo "=============="
    
    for i in {1..10}:
    do
         echo $i
    done


              
    for i in 'ls /boot'     #显示/boot目录下的所有文件
    do
         echo $i
    done


查询空闲IP

    for i in {1..253}
    do
    ping -c1 192.168.1.$i &> /dev/null   #黑洞文件夹
    if [ $? -eq 0 ]
        then
            echo "$i is Busy!"
    else
        echo "$i is Free!"
    fi
    done


判断登录名字脚本

    read -p '>> : ' uname
    case $uname in
    root)
    echo "welcome $uname"
    ;;
    seker)
    echo "welcome $uname"
    ;;
    default)
    echo "welcome $uname"
    ;;
    *)
    echo "no user $uname"
    esac

（6）、函数

    function abc(){
          echo 'aaa' ;
          return 1;  #人为控制返回值
    }
    abc

后面跟参数，选择执行函数

    function aaa(){
            echo 'aaa' ;
    }
    function bbb(){
            echo 'bbb'
    }
    if [ "$1" = 'aaa' ]
    then
     aaa
    elif [ "$1" = 'bbb' ]
    then
        bbb
    else
        echo 'cmd not find'
    fi


（7）、计划任务
安装
yum -y install vixie-cron
yum -y install crontabs

crontab -e -u root   编辑任务 

crontab -l   查看任务内容

\* \* \* \* \* echo 11111 >> /tmp/test.log #每分钟追加到日志里:

tail -f /var/log/cron 查看任务执行情况

![image](https://raw.githubusercontent.com/MMingLeung/Markdown-Picture/master/crontab.png)
