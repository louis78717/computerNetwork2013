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
    def __init__(self,ServerIPaddress=("127.0.0.1",5280)):
        userDict={}
        with SocketContextManager(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(ServerIPaddress)
            sock.settimeout(2.0)
            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    message = message.decode()
                    message,s,name = message.rpartition(' ')
                    message,s,port = message.rpartition('@')
                    if name not in userDict:
                        userDict[name]=(int)(port)
                    print ("%s:"%name,message)
                    message = bytes(name+":"+message,"UTF-8")
                    for user, port in userDict.items():
                        if user != name:
                            sock.sendto(message,("127.0.0.1",port))
                except timeout:
                    continue
class Client(object):
    def __init__(self,ServerIPAddress=("127.0.0.1",5280)):
        with SocketContextManager(AF_INET,SOCK_DGRAM) as sock:
            while True:
                message = bytes(input("Message? "),"UTF-8")
                if not message:break
                sent=sock.sendto(message,ServerIPAddress)
                print ("%i bytes sent"%sent)
                
                
class Client1(object):
    def __init__(self,ServerIPAddress=("127.0.0.1",5280),portNumber=5555):
        quit = False
        username = False
        while True:
            with SocketContextManager(AF_INET,SOCK_DGRAM) as sock2:
                while True:
                    if not username:
                        username = input("Username? ")
                    message = bytes(input(username+": ")+"@"+str(portNumber)+" "+username,"UTF-8")
                    if message.decode()[0:4] == 'quit':
                        quit = True
                        break
                    if not message:break
                    sent=sock2.sendto(message,ServerIPAddress)
            if quit:
                break  
            with SocketContextManager(AF_INET,SOCK_DGRAM) as sock1:
                sock1.bind(("127.0.0.1",portNumber))
                sock1.settimeout(2.0)
                while True:
                    try:
                        message, address = sock1.recvfrom(1024)
                        print (message.decode())
                    except timeout:
                        continue

