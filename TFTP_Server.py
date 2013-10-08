import binascii
from socket import socket as p33socket, AF_INET, SOCK_DGRAM, timeout
#import UDPClient
#from TFTP    import TFTP
#class UDPClient:pass

class UDPServer(p33socket):
    def __exit__(self,argException,argString,argTraceback):
        
        if argException is KeyboardInterrupt:
            print (argString)
            self.close()
            return True
        else:
            super().__exit__(argException,argString,argTraceback)
        pass

class Bit_structure(object):   
    def __init__(self):
        self.transmit_field_offset = 0
        self.bit_fields = bytearray(0)

    def getBitType(self):
        return self.bit_fields

    def register(self,arg_Bit_field_type):
        bdf_type, specified_bdf_offset = arg_Bit_field_type
        self.transmit_field_offset += specified_bdf_offset
        self.bit_fields.extend(Bit_Data_Field(bdf_type,specified_bdf_offset))

#class Bit16(object):
#        def __init__(self,value):

class Bit_field_type(object):
    def __init__(self)      :raise NotImplemented
    def __eq__  (self,other):raise NotImplemented
    def __le__  (self,other):raise NotImplemented
    def __len__ (self)      :raise NotImplemented
    def __repr__(self)      :raise NotImplemented
    def __inv__ (self)      :raise NotImplemented
    def __or__  (self,other):raise NotImplemented
    def __and__ (self,other):raise NotImplemented
    def __xor__ (self,other):raise NotImplemented
    def __add__ (self,other):raise NotImplemented
    def __sub__ (self,other):raise NotImplemented
    def __str__ (self)      :raise NotImplemented


class Bit_field_bit(Bit_field_type):
    def __init__(self,identifier):
        self.identifier = identifier

def IntType(num, length):
    return num,length

def Bit_Data_Field(data, length):

    if type(data)==str:
        binary=bytearray(data,encoding='ascii')
    if type(data)==int:
        binary = bytearray(length)
        if data != 0:
            binary[1]=data
    return binary 

def Ordinal(ordinalType, length):
    value=0
    if ordinalType == "RRQ":
        value = 1
    if ordinalType == "WRQ":
        value = 2
    if ordinalType == "DATA":
        value = 3
    if ordinalType == "ACK":
        value = 4
    if ordinalType == "ERROR":
        value = 5
    return value, length


class TFTP(object):
    def __init__(self):
        pass

    def DATA(self, block=0 ,data=''):
        message = Bit_structure()
        message.register(Ordinal("DATA",2))
        message.register((block,2))
        message.register((data,len(data)*1))
        return str(message.getBitType())

    def ACK(self,message='acknowledge'):
        message = Bit_structure()
        message.register(Ordinal("Ack", 2))
        message.register((message, 2))
        return str(message.getBitType())

    def ERROR(self,errCode,errMessage):
        message = Bit_structure()
        message.register(Ordinal("ERROR", 2))
        message.register(errCode,2)
        message.register(errMessage,len(mode)*1)
        message.register(0,1)
        return str(message.getBitType())

        


class TFTPServer(TFTP):
    "TFTP Server"
    def __init__(self):
        print("Server is running")
        TFTPCommandInterpreter()

        

class TFTPCommandInterpreter(TFTPClient):

    def __init__(self):
        self.serverIP = '10.2.3.4'
        self.serverPort = 55555
        self.commandtable = {
            "help":self.help,
            "pwd":self.pwd,
            "setIP": self.setIP,
            "setPort":self.setPort,
            "cd": self.cd,
            "upload": self.upload,
            "download": self.download,
            "end":self.end
            }
        
        self.wd = "/usr"
        self.notdone = True
        userDict={}
        ServerIPaddress = (self.serverIP,self.serverPort)
        with SocketContextManager(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(ServerIPaddress)
            sock.settimeout(2.0)
            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    message = message.decode()
                    protoOrdinal=message[0:1]
                    if protoOrdinal == 1:
                        ClientFilename=message.[2:message.find('\x00']
                        try:
                            with open(PlatformFilename,"r") as fd:
                                filecontents = fd.read()
                                filelen = len(filecontents)
                                fullblockct, leftoverbytes = divmod(filelen,512)
                                for block in range(fullblockct):
                                    self.DATA(block=block,data=filecontents[block*512,512])
                                    if not self.ACK(): raise TFTPErrorError
                                sock.sendto(bytes(self.DATA(block=len(fullblockct), data=self.DATA),"UTF-8"), address)
                        except:
                            pass 
                    if protoOrdinal == 2:
                         ClientFilename=message.[2:message.find('\x00']
                        try:
                            with open(PlatformFilename,"w") as fd:
                                try:
                                    message, address = sock.recvfrom(1024)
                                    message = message.decode()
                                    messageData = message[4:]
                                    fd.write(messageData)
                                except:
                                    fd.close()
                        except:
                            pass 
                    if protoOrdinal == 4:
                        sock.sendto(bytes('HELLO',"UTF-8"), address)
                    if protoOrdinal == 5:
                        sock.sendto(bytes('That sucks',"UTF-8"), address)

                except timeout:
                    continue

TFTPServer()