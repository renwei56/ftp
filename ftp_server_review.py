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
from time import sleep


HOST="127.0.0.1"
PORT=8885
ADDR=(HOST,PORT)
file_path="/home/tarena/File/"

class MyThread(Thread):
    def __init__(self, connect):
        super().__init__()
        self.connect=connect

    def select_catalog(self):
        list_catalog=os.listdir(file_path)
        if not list_catalog:
            self.connect.send(b"None")
            return
        else:
            self.connect.send(b"Ready")
            catalog="   ".join(list_catalog)
            sleep(0.1)
            self.connect.send(catalog.encode())
            sleep(0.1)
            print("send succefully")


    def download_file(self, info):
        try:
            file=open(file_path+info,"rb")
        except:
            self.connect.send(b"cann't open or find this file ")
            return
        else:
            self.connect.send(b"please ready to accept")
            sleep(0.1)
            while True:
                content=file.read(1024)
                if not content:
                    sleep(0.1)
                    self.connect.send(b"##")
                n=self.connect.send(content)
                print(n)
            file.close()

    def upload_files(self,info):
        pass
    # def wrong(self):
    #     self.connect.send("sorry,please order correctly")

    def run(self) :
        while True:
            data=self.connect.recv(128).decode()
            if data[0]=="S":
                self.select_catalog()
            elif data[0]=="D" :
                self.download_file(data[1:])
            elif data[0]=="U":
                self.upload_files(data[1:])
            else:
                return

def main():
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("waiting for connect")
    while True :
        try:
            connfd,addr=sockfd.accept()
            print("connect from",addr)
        except:
            sys.exit("service out")
        t=MyThread(connfd)
        t.setDaemon(True)
        t.start()
if __name__ == '__main__':
    main()
