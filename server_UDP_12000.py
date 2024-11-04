# server，此端口用于对文本传输进行处理
import os
from socket import *

# 设定端口号为12000
serverPort = 12000
# 创建UDP套接字
serverSocket = socket(AF_INET, SOCK_DGRAM)
# 绑定端口号
serverSocket.bind(('', serverPort))
# 这里直接指定文件的目的文件夹了
folder_path = 'D://to//'
# 测试用
print("服务已成功建立")
# 死循环，开启监听
while True:
    # 显示处于哪个状态用
    print('等待发送文件')
    # 接收文件名和后缀
    file_name , clientAddress_fn = serverSocket.recvfrom(2048)
    # 对文件名和后缀进行解码
    file_name = file_name.decode()
    # 测试用，表示文件名被接收
    print("获得文件标题" , file_name)
    # 接收文件路径，并和文件名进行拼接
    file_path = os.path.join(folder_path, file_name)
    # 接收文件内容
    file_contents, clientAddress_fc = serverSocket.recvfrom(2048)
    # 对文件内容进行解码
    file_contents = file_contents.decode()
    # 测试用，表示文件内容被接收
    print("获得文件内容" , file_contents)
    # 测试用，显示发送方ip和端口号
    print("获得发送方ip和端口号" , clientAddress_fn)

    # 写文件操作
    with open(file_path, 'w') as file:
        file.writelines(file_contents)
        # 测试用
        print("成功写入文件")

    # 关闭文件对象
    file.close()
    # 关闭UDP套接字
    serverSocket.sendto("成功".encode(), clientAddress_fn)