# client端，其中在二进制传输中，实现了类似序号，确认的机制
import os.path
from socket import *
import base64

# 文本传输
def SendTXT(serverName:str , serverPort:int , file_path):
    # 创建UDP套接字，采用IPv4
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # 获得文件名和后缀
    file_name = os.path.basename(file_path)
    # 调试用,打印文件名和后缀
    print(file_name)
    # 创建文件对象，设置为只读
    file = open(file_path , 'r')
    # 读取文件中的所有内容
    contents = file.read()
    # 调试用，打印文件所有内容
    print(contents)

    # 利用创建的UDP套接字来发送文件名及后缀，用的是默认的UTF-8编码，发送到ip为serverName，端口号为serverPort的进程上（请确保对应端口开启了监听模式）
    clientSocket.sendto(file_name.encode(), (serverName, serverPort))
    # 利用创建的UDP套接字发送文件内容
    clientSocket.sendto(contents.encode(), (serverName, serverPort))
    # 等待接收端回传内容到flag_message，同时获取其地址和端口
    flag_message , serverAddr = clientSocket.recvfrom(2048)
    # 解码flag——message中的内容
    flag_message = flag_message.decode()
    # 调试用，用来打印flag_message中的内容
    print(flag_message)
    # 关闭文件对象
    file.close()
    # 关闭套接字
    clientSocket.close()

# 二进制传输
def SendBin(serverName:str , serverPort:int , file_path):
    # 创建TCP套接字
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    # 获得文件名
    file_name = os.path.basename(file_path)
    # 测试用，打印文件名
    print(file_name)
    # 创建文件对象，设置其为二进制只读模式
    with open(file_path, 'rb') as file:
        # 获得文件内容
        contents = file.read()
        # 文件内容进行base64编码
        contents = base64.b64encode(contents)
        # 打印内容，作为测试用
        print(contents)
    # 使用TCP套接字，将内容发送到IP为serverName，端口号为serverPort的进程中
    clientSocket.sendto(file_name.encode(), (serverName, serverPort))
    # 由于二进制文件可能大小过大，因此分报文段来发送
    MAX_DGRAM_SIZE = 2048
    # 模拟sequence.no来发送报文，实际上并没有发送序列号验证，程序只是验证了ack
    # 这里不做sequence的原因是，并未采用滑动窗口，并不是流水线发送文件，同一时间只会有一个报文段处于in-flight状态，不存在所谓的乱序的问题，
    seq = 1
    # 对每个报文进行发送
    for i in range(0 , len(contents), MAX_DGRAM_SIZE):
        # 测试用
        print("发送第" , int(seq) , "个分组")
        # 对内容切片发送
        packet = contents[i:i+MAX_DGRAM_SIZE]
        # 利用TCP套接字发送对应的报文段
        clientSocket.sendto(packet , (serverName, serverPort))
        # 接收server端的ack
        ack , addr = clientSocket.recvfrom(2048)
        # 转为int
        ack = int.from_bytes(ack, byteorder='big')
        #测试用，用于观察ack
        print("接收到ack为" , ack)
        print("期望ack为" , seq + 1)
        # 验证ack是否正确
        if ack == seq + 1 :
            print("接收到ACK,进行下一步传输")
        else:
            print("传输有误，提前停止")
            break
        # 每次循环后序列号要自增
        seq += 1
    # 模拟关闭连接，这里作了简化，只保留了传输FIN来结束传输
    clientSocket.sendto("FIN".encode() , (serverName, serverPort))
    # 对方结束前返回信息，更类似四次握手接收端的ack＋FIN的结合体，但是没有再做验证了
    flag_message, serverAddr = clientSocket.recvfrom(2048)
    flag_message = flag_message.decode()
    print(flag_message)

if __name__ == '__main__':
    # 主程序进行文字引导，输入对应数字进入，分别有三种模式，前两种为主动选择文本传输还是二进制传输，第三种为整个文件夹中的文件自动选择二进制传输或者文本传输
    # 若输入不合法会引导重新输入或主动结束程序
    flag = input("输入相应数字来选择功能:\n1. 文本传输\t2. 二进制文件传输\t3. 传输文件下的多个文件\n")
    while flag != '1' and flag != '2' and flag != '3':
        flag = input("输入相应数字来选择功能:\n1. 文本传输\t2. 二进制文件传输\t3. 传输文件下的多个文件\n")
    if flag == '1':
        mode = input("输入相应数字来选择功能:\n1. 使用实例样本\t2. 使用默认文件夹\t3. 自定义路径\n")
        while flag != '1' and flag != '2' and flag != '3':
            flag = input("输入相应数字来选择功能:\n1. 使用实例样本\t2. 使用默认文件夹\t3. 自定义路径\n")
        if mode == '1' :
            SendTXT('127.0.0.1' , 12000 ,'D://from//tatakai.txt')
        elif mode == '2' :
            file_path = input("请输入文件名:(要求带后缀，并且该文件存在)\n")
            file_path = 'D://from//' + file_path
            SendTXT('127.0.0.1', 12000, file_path)
        elif mode == '3' :
            file_path = input("请输入完整路径名(符合python语法)\n")
            SendTXT('127.0.0.1', 12000, file_path)
    elif flag == '2':
        mode = input("输入相应数字来选择功能:\n1. 使用实例样本\t2. 使用默认文件夹\t3. 自定义路径\n")
        while flag != '1' and flag != '2' and flag != '3':
            flag = input("输入相应数字来选择功能:\n1. 使用实例样本\t2. 使用默认文件夹\t3. 自定义路径\n")
        if mode == '1':
            SendBin('127.0.0.1', 12001, 'D://from//111.docx')
        elif mode == '2':
            file_path = input("请输入文件名:(要求带后缀，并且该文件存在)\n")
            file_path = 'D://from//' + file_path
            SendBin('127.0.0.1', 12001, file_path)
        elif mode == '3':
            file_path = input("请输入完整路径名(符合python语法)\n")
            SendBin('127.0.0.1', 12001, file_path)
    elif flag == '3':
        folder_path = input("请输入指定的文件夹路径(符合python语法)\n")
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            _, file_extension = os.path.splitext(file)
            print(f"File Path: {file_path}")
            print(f"File Type: {file_extension}")
            if file_extension == '.py' or file_extension == 'c' or file_extension == 'cpp' or file_extension == '.txt' or file_extension == '.pdf' or file_extension == '.html' or file_extension == '.htm' or file_extension == '.xml' or file_extension == '.json' or file_extension == '.csv':
                SendTXT('127.0.0.1', 12000, file_path)
            elif file_extension == '.exe' or file_extension == '.docx' or file_extension == '.doc' or file_extension == '.bin' or file_extension == '.dll' or file_extension == '.so' or file_extension == '.dat' or file_extension == '.png' or file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.img' or file_extension == '.mp3' or file_extension == '.mp4':
                SendBin('127.0.0.1', 12001, file_path)
