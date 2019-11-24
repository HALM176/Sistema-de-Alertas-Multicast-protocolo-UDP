#CLIENTE MULTICAST UDP
import socket
import struct
import threading
import time  
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((bind_addr, port))
class Aplicacion():
    
    def __init__(self):

        self.h = threading.Thread(target=self.request)
        self.c2=4
        self.c=0
        self.h.start()
        
        #----------------------------------------------------
        self.raiz = Tk() 
        self.raiz.geometry('350x430')
        self.raiz.title('Receptor') 
        self.raiz.configure(bg="black") 
        self.raiz.resizable(width=False, height=False)
        #---------------------------------------
        self.valorVariable= DoubleVar()
        self.set2 = int() 
        self.etiquetaVariable=StringVar()
        self.con=StringVar()
        #----------------------------------------
        self.tinfo = Text(self.raiz,width=1,height=20,bg="black",spacing2=4)
        self.tinfo.grid(row=1,column=0,columnspan=3,sticky=E+W)
        #--------------------------------------------------------
        self.en =Entry(self.raiz,textvariable=self.set2)
        self.en.grid(row=2,column=1,pady=3,padx=2) 
        #-------------------------------------------------------------
        self.et1 =Label(self.raiz,bg="orange",width=51,height=2,text="MULTICAST")
        self.et1.grid(row=0,column=0,columnspan=3,sticky=W+E)
        #---------------------------------------------------
        self.set=Label(self.raiz, text="SET", foreground="yellow", background="black" )
        self.set.grid(row=2,column=0)
        #---------------------------------------------------------
        self.temperatura=Label(self.raiz, textvariable = self.etiquetaVariable, foreground="yellow", background="black" )
        self.temperatura.grid(row=3,column=0,columnspan=3,pady=4,padx=12)
        #-------------------------------------------------------------
        self.bmodificar = Button(self.raiz,bg="red", bd=5,text='modificar',command=self.salir)                            
        self.bmodificar.grid(row=2,column=2)


        self.photo2= PhotoImage(file='./alerta.png')
        self.photo1= PhotoImage(file='./ok.gif')
        self.raiz.mainloop()

    def request(self):
        while True:
            if self.c2>0:
                message, address = sock.recvfrom(255)
                temp=int(message.decode("utf-8"))
                self.etiquetaVariable.set(str(temp)+ " °C")
                print(self.set2)
                self.r="h"
                if self.set2 !=0:  
                    if temp >=self.set2:
                        print("peligro")
                        control="peligro"
                    if temp < self.set2:
                        control="ok"
                        print("ok")
                   
                    if self.c==0:
                        if control=="peligro" :
                            self.tinfo.delete(1.0,END)
                            self.tinfo.image_create(END, image=self.photo2)
                            self.tinfo.insert(INSERT,'\n')
                            message=b""
                            self.r = mb.askquestion("Pregunta!", "¿Quieres silenciar la alarma?")
                    if control=="ok":
                        self.tinfo.delete(1.0,END)
                        self.c=0
                        self.tinfo.image_create(END, image=self.photo1)
                        self.tinfo.insert(INSERT,'\n')
                        time.sleep(1)
                        message=b""                 
                        self.r="h"

    
            if self.r=="yes":
                self.c=4
            if self.r=="no":
                message=b""
                self.tinfo.delete(1.0,END)
                time.sleep(2)


    def salir(self):
        self.set2=int(self.en.get())


def main(): #define el metodo principal 
    mi_app = Aplicacion()#instancia el objeto de la clase aplicacion 
    return 0

if __name__ == '__main__':
    main()
    