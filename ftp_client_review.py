"""
ftp 文件服务器分析
【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
【2】 客户端可以查看服务器文件库中有什么文件。
【3】 客户端可以从文件库中下载文件到本地。
【4】 客户端可以上传一个本地文件到文件库。
【5】 使用print在客户端打印命令输入提示，引导操作
"""
import sys
from socket import *
from threading import Thread
import  os


HOST="127.0.0.1"
PORT=8885
ADDR=(HOST,PORT)
file_path="/home/tarena/File-copy/"

def print_order():
    print("=== S:select catalog ===")
    print("=== D:download file ===")
    print("=== U:upload file ===")
    print("=== exit:quit ===")

class Manage:
    def __init__(self,confd):
        self.confd=confd
    def s_manage(self):
        # print("1")
        self.confd.send(b"S")
        # print("2")
        data=self.confd.recv(30).decode()
        # print("3")
        if data == "Ready" :
            # while True:
                data = self.confd.recv(10240).decode()
                # if not data:
                #     break
                print(data)
        # return
        else:
            print("None")


    def d_manage(self):
        file_name = input("please input file name>>")
        self.confd.send(("D"+file_name).encode())
        file=open(file_path+file_name,"wb")
        data=self.confd.recv(100).decode()
        print(data)
        while True:
            data=self.confd.recv(1024)
            if not data:
                file.close()
                return
            file.write(data)
            file.flush()
    def u_manage(self):
        pass


def main():
    sockfd = socket()
    sockfd.connect(ADDR)
    print("all ready")
    print_order()
    m = Manage(sockfd)
    while True:
        order=input("please input orders >>")
        if order=="S":
            m.s_manage()
        elif order=="D":
            m.d_manage()
        elif order=="U":
            m.u_manage()
        elif order=="exit":
            sockfd.close()
        else :
            print("please input order correctly")

if __name__ == '__main__':
    main()