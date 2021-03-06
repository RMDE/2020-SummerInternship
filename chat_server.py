import socket
from time import sleep
from event import *
from gui import *
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QDesktopWidget, QMessageBox,
        QTextEdit,QLabel,QPushButton, QApplication,QMainWindow, QAction, qApp,
        QHBoxLayout, QVBoxLayout,QGridLayout,QLineEdit)
from PyQt5.QtGui import QFont,QIcon,QPixmap,QPalette,QColor
from PyQt5.QtCore import QCoreApplication,Qt
import threading

SIZE = 1024

def send():
    global ip,port,server,snd,Window
    data = snd.text()
    print("sendto "+str(ip)+":"+str(port)+"  : "+data)
    try:
        server.sendto(bytes(data,encoding='utf-8'),(ip,port))
    except:
        Error(Window,"Message send fails")

def receive():
    global server,msg,ip,port,Window,lbl
    while Window.flag:
    	data,address = server.recvfrom(SIZE)
    	if Window.flag == False:
    	    return
    	ip = address[0]
    	port = address[1]
    	msg.setText("receive : "+str(data))
    	lbl.setText("对象 : "+str(ip)+" : "+str(port))
    	# print("recfrom"+str(address)+": "+str(data))

def init(ip,port):
    global server,Window
    address = (ip,port)
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        server.bind(address)
    except:
        Error(Window,"socket fails!")

def gui():
    global msg,snd,lbl,Window
    Window = Gui()
    Window.resize(600,400)
    Window.center()
    Window.setWindowTitle('Server聊天窗口')
    Window.setWindowOpacity(0.97)
    lbl = Window.Label("对象: ",100,30,50,400,"black",20)
    msg = Window.Label("NULL",50,100,50,400,"black",20,"white")
    snd = Window.Input(50,200,h=50,w=400)
    btn = Window.Button('发送',470,200,send,50,70,"white","#6DDF6D",30)
    Window.show()


if __name__=='__main__':
    global Window,ip,port
    app = QApplication(sys.argv)
    _ip = '127.0.0.1'
    _port = 9090
    init(_ip,_port)
    gui()
    print("start")
    th = threading.Thread(target=receive)
    th.start()
    sys.exit(app.exec_())
    server.close()
