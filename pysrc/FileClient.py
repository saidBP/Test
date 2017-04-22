

# -*- coding:utf-8 -*- 
#file:FileClient.py
#

import Tkinter
import tkFileDialog
import socket
import os
class Window:
    def __init__(self, root):
        label1=Tkinter.Label(root, text='IP')
        label2=Tkinter.Label(root, text='Port')
        label3=Tkinter.Label(root, text='File')
        label1.place(x=5,y=5)
        label2.place(x=5,y=30)
        label3.place(x=5,y=55)
        self.entryIP = Tkinter.Entry(root)
        self.entryIP.insert(Tkinter.END, '127.0.0.1')
        self.entryPort = Tkinter.Entry(root)
        self.entryPort.insert(Tkinter.END, '1051')
        self.entryData = Tkinter.Entry(root)
        self.entryData.insert(Tkinter.END, 'Hello')
        self.entryIP.place(x=40, y=5)
        self.entryPort.place(x=40, y=30)
        self.entryData.place(x=40, y=55)
        self.send=Tkinter.Button(root, text='senf file', command=self.Send)
        self.openfile=Tkinter.Button(root, text='find', command=self.Openfile)
        self.send.place(x=40,y=80)
        self.openfile.place(x=170,y=55)
    def Send(self):
        try:
            ip=self.entryIP.get()
            port=int(self.entryPort.get())
            filename=self.entryData.get()
            tt=filename.split('/')
            name=tt[len(tt)-1]
            client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            client.send(name)
            file=os.open(filename, os.O_RDONLY|os.O_EXCL|os.O_BINARY)
            while 1:
                data=os.read(file, 1024)
                if not data:
                    break
                client.send(data)
            os.close(file)
            client.close()
        except:
            print('send error')
    def Openfile(self):
        r = tkFileDialog.askopenfilename(title='Python Tkinter', filetypes=[('All files', '*'),('Python', '*.py *.pyw')])
        if r:
            self.entryData.delete(0, Tkinter.END)
            self.entryData.insert(Tkinter.END, r)
root = Tkinter.Tk()
window = Window(root)
root.mainloop()
