import serial
import time
import threading
from tkinter import *
from tkinter import ttk
import socket
import struct

cserial=serial.Serial('COM4',baudrate=9600,timeout=1)
multicast_addr = '224.0.0.1'
port = 6000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

class Aplicacion():
    
    def __init__(self):

        self.c=4
        self.k=0
        self.c2=34
        self.h = threading.Thread(target=self.request)
        self.h.start()
        #----------------------------------------------------
        self.raiz = Tk() 
        self.raiz.geometry('500x430')
        self.raiz.title('emisor') 
        self.raiz.configure(bg="black") 
        self.raiz.resizable(width=False, height=False)
        #---------------------------------------
        self.valorVariable= DoubleVar()
        self.etiquetaVariable=StringVar()
        self.con=StringVar()
        #----------------------------------------
        self.temperatura=Label(self.raiz, textvariable = self.etiquetaVariable, foreground="yellow", background="black" )
        self.temperatura.grid(row=2, column=0,rowspan=2)
        #----------------------------------------
        self.barr=ttk.Progressbar(self.raiz,orient="vertical",length=300, mode="determinate",maximum=40,variable=self.valorVariable)
        self.barr.grid(row=3,column=1)
        #-------------------------------------------------------------------  
        self.et1 =Label(self.raiz,bg="orange",width=71,height=2,text="MULTICAST")
        self.et1.grid(row=0,column=0,columnspan=3,sticky=W+E)
        #-------------------------------------------------------------
        self.et1 =Label(self.raiz,bg="gray",width=71,height=2,textvariable=self.con)
        self.et1.grid(row=1,column=0,columnspan=3)
        #-------------------------------------------------------------
        self.bsalir = Button(self.raiz,bg="red", bd=5,text='Salir y desconectar multicast',width=30,height=1,command=self.salir)                            
        self.bsalir.grid(row=4,column=1,pady=4,padx=12)
        #------------------------------------------------
        self.raiz.mainloop()

    def request(self):
        while True:
            if self.c>0:
                self.data=cserial.readline()
                self.valorVariable.set(self.data.decode("utf-8"))
                self.u=float(self.data.decode("utf-8"))
                self.h=int(self.u)
                self.etiquetaVariable.set(str(self.h)+" °C")
                self.k=self.k+1
                self.con.set("Lectura: "+ str(self.k))
                sock.sendto(str.encode(str(self.h)), (multicast_addr, port))
                print(str(self.u))
                time.sleep(2)
            if self.c==0:
                break

    def salir(self):
    	self.c=0
    	self.raiz.destroy()
          

def main(): #define el metodo principal 
    mi_app = Aplicacion()#instancia el objeto de la clase aplicacion 
    return 0

if __name__ == '__main__':
    main()
	