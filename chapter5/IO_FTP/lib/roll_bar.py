import sys

def roll_bar(recv_size, filesize):
    '进度条'
    size = float(recv_size) / float(filesize) * 100
    p = "\r%d%% :%s" % (size, int(size) * '*')
    sys.stdout.write(p)
    sys.stdout.flush()