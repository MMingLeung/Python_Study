import subprocess
import paramiko


mode = 'salt' # ssh, agent

#需要中控机和连接主机名IP
if mode == 'salt':
    v1 = subprocess.getoutput('salt "xx" cmd.run "%s" ' % 'ifconfig')
    v2 = subprocess.getoutput('salt "xx" cmd.run "%s" ' % 'ls')
    v3 = subprocess.getoutput('salt "xx" cmd.run "%s" ' % 'df')

elif mode == 'ssh':
    private_key = paramiko.RSAKey._from_private_key_file('xx')
    # 连接ssh
    ssh = paramiko.SSHClient
    # 允许连接不在know_hosts文件的机器
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='c1.salt.com', port=22, username='a1', password='123')
    stdin, stdout, stderr = ssh.exec_command('df')
    result = stdout.read()
    ssh.close()

else:
    v1 = subprocess.getoutput('ifconfig')
    v2 = subprocess.getoutput('ls')
