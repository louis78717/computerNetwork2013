from socket import socket as p33socket, AF_INET, SOCK_DGRAM, timeout
print ("p33socket=%r,AF_INET=%r,SOCK_DGRAM=%r"%(p33socket,AF_INET,SOCK_DGRAM))

class SocketContextManager(p33socket):
    def __exit__(self,argException,argString,argTraceback):
        
        if argException is KeyboardInterrupt:
            print (argString)
            self.close()
            return True
        else:
            super().__exit__(argException,argString,argTraceback)
        pass

class Server(object):
    def __init__(self,ServerIPaddress=("10.27.8.42",5280)):
        userDict={}
        with SocketContextManager(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(ServerIPaddress)
            sock.settimeout(2.0)
            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    message = message.decode()
                    message,s,name = message.rpartition(' ')
                    if name not in userDict:
                        userDict[name]=address
                    print ("%s:"%name,message)
                    message = bytes(name+": "+message,"UTF-8")
                    for user, port in userDict.items():
                        if user != name:
                            sock.sendto(message,port)
                except timeout:
                    continue
                
class Client(object):
    def __init__(self,ServerIPAddress=("10.27.8.42",5280)):
        quit = False
        username = False
        while True:
            with SocketContextManager(AF_INET,SOCK_DGRAM) as sock:
                sock.settimeout(.2)
                while True:
                    if not username:
                        username = input("Username? ")
                    message = bytes(input(username+": ")+" "+username,"UTF-8")
                    if len(message) > len(username)+1:
                        if message.decode()[0:4] == 'quit':
                            quit = True
                            break
                        if not message:break
                        sent=sock.sendto(message,ServerIPAddress)
                    hasmessage = True
                    try:
                        while hasmessage:
                            message, address = sock.recvfrom(1024)
                            print (message.decode())
                    except timeout:
                        hasmessage = False
                        continue
            if quit:
                break 

