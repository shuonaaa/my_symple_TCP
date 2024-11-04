# server
import os
from socket import *
import base64

# 设定端口号为12001
serverPort = 12001
# 创建TCP套接字
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

    # 模拟缓存用，来存取二进制内容
    buffer = b''
    # 模拟发送的ack
    i = 1
    while True:
        while True:
            # 测试用，显示接收的i个分组
            print("第" , int(i) , "个分组")
            # 自增i用来当ack
            i += 1
            # 接收内容
            contents = serverSocket.recv(2048)
            # 测试用，打印接收内容
            print(contents)
            # 若发送方发送FIN，立即结束
            if contents == b'FIN' :
                break
            # 将内容加入到缓存中
            buffer += contents
            print("获得文件内容" , contents)
            # 转成转换为指定长度和字节顺序的字节数组
            ack_to_send = (i).to_bytes(4, byteorder='big')
            # 测试用
            print("成功发送ack", i)
            # 发送ack到发送端
            serverSocket.sendto(ack_to_send,clientAddress_fn)
        # 每次都重置ack，这里的ack更像一直relative ack，是相对的，都是从1开始
        i = 1
    # 对缓存进行base64解码
    buffer = base64.b64decode(buffer)

    # 写文件操作
    with open(file_path, "wb") as file:
        file.write(buffer)
        # 关闭文件对象
        file.close()
    # 测试用，显示发送方ip和端口号
    print("获得发送方ip和端口号" , clientAddress_fn)
    # 关闭TCP套接字
    serverSocket.sendto("成功".encode(), clientAddress_fn)