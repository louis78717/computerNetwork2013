from socket import socket as p33socket, AF_INET, SOCK_DGRAM, timeout
print ("p33socket=%r,AF_INET=%r,SOCK_DGRAM=%r"%(p33socket,AF_INET,SOCK_DGRAM))

class SocketContextManager(p33socket):
    def __exit__(self,argExeception,argString,argTraceback):
        
        if argException is KeyboardInterrupt:
            print (argString)
            self.close()
            return True
        else:
            super().__exit__(arg.Exception,argString,argTraceback)
        pass

class Server(object):
    def __init__(self,ServerIPaddress=("127.0.0.1",5280)):
        userDict={}
        with p33socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(ServerIPaddress)
            sock.settimeout(2.0)
            while True:
                try:
                    if address[1] not in userDict:
                        messagePart=message.decode().split()
                        userDict[address[1]]=(messagePart[0],messagePart[1])
                    else: 
                        message, address = sock.recvfrom(1024)
                        print ("%s:"%userDict[address[1]][0],message.decode)
                        message = bytes(userDict[address[1]][0]+":"+message.decode,"UTF-8")
                        sock.sendto(("127.0.0.1",userDict[address[1]][1])
                except timeout:
#                    print (".",end="")
                    continue
class Client(object):
    def __init__(self,ServerIPAddress=("127.0.0.1",5280)):
        with p33socket(AF_INET,SOCK_DGRAM) as sock:
            while True:
                message = bytes(input("Message? "),"UTF-8")
                if not message:break
                sent=sock.sendto(message,ServerIPAddress)
                print ("%i bytes sent"%sent)
                
                
class Client1(object):
    def __init__(self,ServerIPAddress=("127.0.0.1",5280),portNumber=5555)):
        while True:
            with p33socket(AF_INET,SOCK_DGRAM) as sock1:
                sock1.bind(("127.0.0.1",portNumber)
                sock1.settimeout(2.0)
                while True:
                    message, address = sock.recvfrom(1024)
                    print (message.decode)
            with p33socket(AF_INET,SOCK_DGRAM) as sock2:
                while True:
                    message = bytes(input("Message? "),"UTF-8")
                    if not message:break
                    sent=sock2.sendto(message,ServerIPAddress)
#                    print ("%i bytes sent"%sent)
                



            
        
