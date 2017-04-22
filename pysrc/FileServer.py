

# -*- coding:utf-8 -*- 
#file:FileServer.py
#

import Tkinter
import threading
import socket
import os

class ListenThread(threading.Thread):
    def __init__(self, edit, server):
        threading.Thread.__init__(self)
        self.edit=edit
        self.server=server
        self.files=['FileServer.py']
    def run(self):
        while 1:
            try:
                self.client, addr = self.server.accept()
                self.edit.insert(Tkinter.END, 'connect from:%s:%d\n' % addr)
                data = self.client.recv(1024)
                self.edit.insert(Tkinter.END, 'recv file:%s \n' % data)
                file = os.open(data, os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_BINARY)
                while 1:
                    rdata = self.client.recv(1024)
                    if not rdata:
                        break
                    os.write(file, rdata)
                os.close(file)
                self.client.close()
                self.edit.insert(Tkinter.END, 'close connect\n')
            except:
                self.edit.insert(Tkinter.END, 'close connect\n')
                break
class Control(threading.Thread):
    def __init__(self, edit):
        threading.Thread.__init__(self)
        self.edit=edit
        self.event=threading.Event()
        self.event.clear()
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', 1051))
        server.listen(1)
        self.edit.insert(Tkinter.END, 'waiting for connection\n')
        self.lt = ListenThread(self.edit, server)
        self.lt.setDaemon(True)
        self.lt.start()
        self.event.wait()
        server.close()
    def stop(self):
        self.event.set()
class Window:
    def __init__(self, root):
        self.root=root
        self.butlisten=Tkinter.Button(root, text='start listening', command=self.Listen)
        self.butlisten.place(x=20,y=15)
        self.butclose=Tkinter.Button(root, text='close listening', command=self.Close)
        self.butclose.place(x=120,y=15)
        self.edit=Tkinter.Text(root)
        self.edit.place(y=50)
    def Listen(self):
        self.ctrl=Control(self.edit)
        self.ctrl.setDaemon(True)
        self.ctrl.start()
    def Close(self):
        self.ctrl.stop()
root=Tkinter.Tk()
window=Window(root)
root.mainloop()
    

