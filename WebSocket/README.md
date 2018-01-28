# WebSocket

## 一、定义

WebSocket 是基于 TCP/IP 协议，可在单个 TCP 连接上进行全双工通信的协议。使服务端与客户端之间的数据交互变得更简单，允许服务器主动向客户端推送数据，只要完成一次握手，两者就可以创建持久性的连接，并进行双向的数据传输。



## 二、内部原理

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/websocket1.png?raw=true)



**客户端**

````Html
...
// 客户端发起连接请求
<script>
     var webSocket = new WebSocket('ws://127.0.0.1:8030');
</script>

...
````



**服务端**

````python
#!usr/bin/env python
#! -*- coding: utf-8 -*-
import socket
import hashlib
import base64
import struct


# 处理请求头函数
def get_header(header_bytes):
    headers_str = header_bytes.decode('utf-8')

    header, body = headers_str.split('\r\n\r\n', 1)

    header_list = header.split('\r\n')

    header_dict = {}
    for i in range(len(header_list)):
        if i == 0:
            header_dict['method'], header_dict['url'], header_dict['protocol']= header_list[i].split(' ')
        elif i == 1:
            header_dict['host'] = header_list[i].split(': ')[1]
        else:
            header_split_list = header_list[i].split(': ')
            header_dict[header_split_list[0]] = header_split_list[1]
    return header_dict

def get_msg(msg):
    # 解密
    # 第二个字节的后7位
    print('收到数据',msg)
    payload_len = msg[1] & 127

    if payload_len == 126:
        ex_payload_len = msg[2:4]
        mask = msg[4:8]
        decoded = msg[8:]
    elif payload_len == 127:
        ex_payload_len = msg[2:10]
        mask = msg[10:14]
        decoded = msg[14:]
    else:
        ex_payload_len = None
        mask = msg[2:6]
        decoded = msg[6:]

    bytes_list = bytearray()
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    body = bytes_list.decode('utf-8')
    return body  
  
def send_msg(msg_bytes, conn):
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.send(msg)
    return True
  
# 创建 socket 对象，绑定 ip, port，监听
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8090))
sock.listen(5)

conn, addr = sock.accept()

# 接收客户端连接请求
data = conn.recv(8096)

# 处理请求头
header_dict = get_header(data)

# websocket magic_string
magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
# 拼接请求头中 Sec-WebSocket-Key 和 magic_string
value = header_dict['Sec-WebSocket-Key'] + magic_string
# 连接的密文
sec_value = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())

response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
"Upgrade:websocket\r\n" \
"Connection: Upgrade\r\n" \
"Sec-WebSocket-Accept: {swa}\r\n" \
"WebSocket-Location: ws://{host}{url}\r\n\r\n"


# 按指定格式返回给客户端
response = response_tpl.format(swa=sec_value.decode('utf-8'), host=header_dict['host'], url=header_dict['url'])
conn.send(response.encode('utf-8'))

# 连接成功后循环接收请求
while True:
    try:
        msg = conn.recv(8096)
    except Exception as e:
        msg = None
    if not msg:
        break
	
    # 处理接收的加密信息
    body = get_msg(msg)
	
    # 以规定的格式发送信息
    send_msg(body.encode('utf-8'), conn)

sock.close()
````



## 三、基于 Tornado WebSocket 开发聊天室

**见 /char_room**