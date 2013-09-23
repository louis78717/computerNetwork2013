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
        with p33socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(ServerIPaddress)
            sock.settimeout(2.0)
            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    print ("Message from %r: %s:"%address,message )
                except timeout:
                    print (".",end="")
                    continue
class Client(object):
    def __init__(self,ServerIPAddress=("127.0.0.1",5280)):
        with p33socket(AF_INET,SOCK_DGRAM) as sock:
            while True:
                message = bytes(input("Message? "),"UTF-8")
                if not message:break
                sent=sock.sendto(message,ServerIPAddress)
                print ("%i bytes sent"%sent)
                
                
            



            
        
