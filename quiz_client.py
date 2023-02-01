import socket 
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

# nickname = input("Choose your nickname: ")
client.connect((ip_address,port))
print("Connected to the server")




class GUI:

    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=400)

        self.login.title("Login")
        self.pls = Label(self.login,text="Please login to continue",justify=CENTER,font="Helvetica 14 bold")
        self.pls.place(relheight = 0.15,relx=0.2,height=0.07)

        self.labelName = Label(self.login,text="Name: ",font="Helvetica 12")
        self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)

        self.entryName = Entry(self.login,font="Helvetica 12")
        self.entryName.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.2)
        self.entryName.focus()

        self.submit = Button(self.login,text="Continue",font="Helvetica 13",command=lambda:self.goAhead(self.entryName.get()))
        self.submit.place(relx=0.4,rely=0.55)

        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()       
        self.layout(name)
        rcv=Thread(target=self.receive)
        rcv.start()

    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.resizable(width=False,height=False)  
        self.Window.configure(width=500,height=600,bg="grey")
        self.Window.title("QUIZ GAME")

        self.labelHead = Label(self.Window,text=self.name, bg="black", fg="white", font="Helvetica 12 bold", pady=5 )
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window,width=480,bg="white")
        self.line.place(relwidth=1,relheight=0.1,rely=0.09)

        self.textCons = Text(self.Window,width=20,height=2, bg="grey",fg="black", font="Ariel 12", padx=5, pady=5)
        self.textCons.place(relheight=0.6, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window,bg="white",height=80)
        self.labelBottom.place(relwidth=1,rely=0.8)

        
        self.entryMsg = Entry(self.labelBottom, bg="grey", fg="black", font="Helvetica 13")
        self.entryMsg.focus()
        self.entryMsg.place(relwidth=0.7, relheight=0.06,relx=0.04,rely=0.03)

        self.buttonMsg = Button(self.labelBottom,text="Submit", width=20, bg="grey", fg="white",command=lambda:self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.75,rely=0.03,relheight=0.06,relwidth=0.2)

        self.textCons.config(cursor="arrow")

        scrollBar = Scrollbar(self.textCons)
        scrollBar.place(relheight=1,relx=0.9)

        scrollBar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def sendButton(self,msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0,END)
        snd = Thread(target=self.write)
        snd.start()

       
    def receive(self):
        while True:
            try:
                msg=client.recv(2048).decode("utf-8")
                if msg=="NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.showMsg(msg)
                    
            except:
                print("An error occured!")            
                client.close()
                break

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode("utf-8"))       
            self.showMsg(message)
            break

    def showMsg(self,msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,msg+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

        

g = GUI()
