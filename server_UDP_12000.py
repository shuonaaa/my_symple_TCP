# server
import os
from socket import *


serverPort = 12000
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
    file_contents, clientAddress_fc = serverSocket.recvfrom(2048)
    file_contents = file_contents.decode()
    print("获得文件内容" , file_contents)
    print("获得发送方ip和端口号" , clientAddress_fn)


    with open(file_path, 'w') as file:
        file.writelines(file_contents)
        print("成功写入文件")
        # keyword = input("保留文件? (Y/N)")
        # while keyword != 'y' and keyword != 'Y' and keyword != 'n' and keyword != 'N':
        #     keyword = input("保留文件? (Y/N)")
        # if keyword == 'y' or keyword == 'Y':
        #     print("保留文件")
        # else:
        #     file.close()
        #     os.remove(file_path)
        #     print("已删除文件")
    file.close()
    serverSocket.sendto("成功".encode(), clientAddress_fn)