# client
import os.path
from socket import *
import base64


def SendTXT(serverName:str , serverPort:int , file_path):
    clientSocket = socket(AF_INET, SOCK_DGRAM)


    # file_path = 'D://from//tatakai.txt'
    file_name = os.path.basename(file_path)
    print(file_name)
    file = open(file_path , 'r')
    contents = file.read()
    print(contents)

    clientSocket.sendto(file_name.encode(), (serverName, serverPort))
    clientSocket.sendto(contents.encode(), (serverName, serverPort))
    flag_message , serverAddr = clientSocket.recvfrom(2048)
    flag_message = flag_message.decode()
    print(flag_message)
    file.close()
    clientSocket.close()

def SendBin(serverName:str , serverPort:int , file_path):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    # file_path = 'D://from//111.docx'
    # file_path = 'D://from//el.jpg'
    file_name = os.path.basename(file_path)
    print(file_name)
    with open(file_path, 'rb') as file:
        contents = file.read()
        contents = base64.b64encode(contents)
        print(contents)
    clientSocket.sendto(file_name.encode(), (serverName, serverPort))
    MAX_DGRAM_SIZE = 2048
    seq = 1
    for i in range(0 , len(contents), MAX_DGRAM_SIZE):
        print("发送第" , int(seq) , "个分组")
        packet = contents[i:i+MAX_DGRAM_SIZE]
        # print(packet)
        clientSocket.sendto(packet , (serverName, serverPort))
        ack , addr = clientSocket.recvfrom(2048)
        ack = int.from_bytes(ack, byteorder='big')
        print("接收到ack为" , ack)
        print("期望ack为" , seq + 1)
        if ack == seq + 1 :
            print("接收到ACK,进行下一步传输")
        else:
            print("传输有误，提前停止")
            break
        seq += 1
    clientSocket.sendto("FIN".encode() , (serverName, serverPort))
    flag_message, serverAddr = clientSocket.recvfrom(2048)
    flag_message = flag_message.decode()
    print(flag_message)

if __name__ == '__main__':
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
