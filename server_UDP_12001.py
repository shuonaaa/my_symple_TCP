# server
import os
from socket import *
import base64

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
folder_path = 'D://to//'
print("服务已成功建立")
while True:
    print('等待发送文件')
    file_name , clientAddress_fn = serverSocket.recvfrom(2048)
    file_name = file_name.decode()
    print("获得文件标题" , file_name)
    file_path = os.path.join(folder_path, file_name)

    buffer = b''
    i = 1
    while True:
        print("第" , int(i) , "个分组")
        i += 1
        contents = serverSocket.recv(2048)
        print(contents)
        if contents == b'FIN' :
            break
        buffer += contents
        print("获得文件内容" , contents)
        ack_to_send = (i).to_bytes(4, byteorder='big')
        print("成功发送ack", i)
        serverSocket.sendto(ack_to_send,clientAddress_fn)
    buffer = base64.b64decode(buffer)
    with open(file_path, "wb") as file:
        file.write(buffer)
        file.close()
    print("获得发送方ip和端口号" , clientAddress_fn)
    serverSocket.sendto("成功".encode(), clientAddress_fn)