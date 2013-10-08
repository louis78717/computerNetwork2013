import binascii
from socket import socket as p33socket, AF_INET, SOCK_DGRAM, timeout
#import UDPClient
#from TFTP    import TFTP
#class UDPClient:pass

class UDPClient(p33socket):
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

    def RRQ(self,fileName='',mode='NETASCII'):
        message = Bit_structure()
        message.register(Ordinal("RRQ", 2))
        message.register((fileName,len(fileName)*1))
        message.register((0,1))
        message.register((mode,len(mode)*1))
        message.register((0,1))
        return str(message.getBitType())

    def WRQ(self,fileName='',mode='NETASCII'):
        message = Bit_structure()
        message.register(Ordinal("WRQ", 2))
        message.register((fileName,len(fileName)*1))
        message.register((0,1))
        message.register((mode,len(mode)*1))
        message.register((0,1))
        print(str(message.getBitType()))
        return str(message.getBitType())

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

        


class TFTPClient(TFTP):
    "TFTP Client"
    def __init__(self):
        
    
        
        print ("""
TFTP Client.

Enter help for help.

""")

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
        
        while self.notdone:

            self.userinput = input(""">>> """)

            cp  = self.userinput.strip(" ").split(" ")
            command, param = cp[0],cp[-1]

            if not command in self.commandtable:
                print ("Command error.")
                continue

            self.notdone = self.commandtable[command](param)
              
          

    def cd(self,wd):
        self.wd = wd.strip("'")
        return self.pwd("")

    def pwd(self,noparam):
        print(self.wd)
        return True

    def setIP(self,IP):
        self.serverIP = IP
        print (self.serverIP)
        return True

    def setPort(self,port):
        self.serverPort = port
        print (self.serverPort)
        return True

    def end(self,noparam):
        return False  # not notdone

    def upload(self,filename):  # send file from client to server
        
        TFTPIPaddress = self.serverIP
        TFTPPORT=self.serverPort
        TFTP_Address = (TFTPIPaddress,TFTPPORT)
        PlatformFilename = 'test.txt'
        with UDPClient() as sock:
            with open(PlatformFilename,"r") as fd:
                sock.sendto(bytes(self.WRQ(PlatformFilename),"UTF-8"), TFTP_Address)
                payload, ServerIPAddress = sock.recv(1024)

                filecontents = fd.read()
                filelen = len(filecontents)
                fullblockct, leftoverbytes = divmod(filelen,512)
                
                for block in range(fullblockct):
                    self.DATA(block=block,data=filecontents[block*512,512])
                    if not self.ACK(): raise TFTPErrorError
                sock.sendto(bytes(self.DATA(block=len(fullblockct), data=self.DATA),"UTF-8"), TFTP_Address)
                # self.DATA(block,
                #           leftoverbytes,
                #           filecontents[-leftoverbytes:]
                #           )

                if not self.ACK():
                    raise TFTPErrorError

                self = True  # to thine own ...
                        
    def download(self,filename):
     #"Send filename  from TFTP client to TFTP server."
        with UDPClient() as sock:
            with open(PlatformFilename,"W") as fd:
                            
        #bug: we should test to be sure PlatformFilename's not there before we
        # write.  We really need a strict creat.

                self.RRQ(filename)

                filecontents = bytearray([])
                block = self.Data()
                while 512 == len(block):
                    filecontents.append(block)
                    block = self.Data()
                filecontents.append(block) # the short block is the ACK

                fd.write(filecontents)

            return True

    def help(self,*param,**xdict):
        print ("""


pwd                                     # >>> pwd
                                        # usr/george/
setIP    TCP.server.IP.address          # >>> setIP  10.2.3.4 
                                        # 10.2.3.4  
setPort  TCP.server.Port.address        # >>> setPort  5000 
                                        # 5000  
cd       'path'                         # >>> cd '/projectb/'
                                        # /projectb/
upload   'filename'                     # >>> upload 'test.txt'
                                        # text.txt uploaded
download 'filename'                     # >>> download 'newtest.txt'
                                        # newtest.txt downloaded 
exit

>>> """)
        return True

TFTPClient()
