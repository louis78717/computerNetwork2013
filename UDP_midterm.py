from socket import socket as p33socket, AF_INET, SOCK_DGRAM, timeout

class UDPClient(p33socket):
    def __init__(self):
        self.Addr           #IP address of the current machine
        self.protocol       #Protocol of the data sent
        self.Port           #Port number of the current machine

    def __exit__(self,argException,argString,argTraceback):
        
        if argException is KeyboardInterrupt:
            print (argString)
            self.close()
            return True
        else:
            super().__exit__(argException,argString,argTraceback)
        pass

    def sendto(self, data, address):
        self.sourceAddr = self.Addr                     #line 83     the addr of the machine that the data is sent from 
        self.destinationAddr = address[0]               #line 84
        self.protocol = self.protocol                   #line 87
        self.UDPLength = len(data)                      #line 87
        self.sourcePort = self.Port                     #Line 31     the port of the machine that the data is sent from
        self.destinationPort = address[1]               #Line 31
        self.Length = len(data)                         #line 35
        self.data = data                                #line 37
        '''
            The next step would to take these attributes and format them into the following wire format 
            and then send it out from the socket (from line 29 and 81): 

                 0      7 8     15 16    23 24      31
                 +--------+--------+--------+--------+
                 |          source address           |
                 +--------+--------+--------+--------+
                 |        destination address        |
                 +--------+--------+--------+--------+
                 |  zero  |protocol|   UDP length    |
                 +--------+--------+--------+--------+
                 |     Source      |   Destination   |
                 |      Port       |      Port       |
                 +--------+--------+--------+--------+
                 |                 |                 |
                 |     Length      |    Checksum     |
                 +--------+--------+--------+--------+
                 |                                     
                 |          data octets ...            
                 +---------------- ...                 


        '''
        
    def recvfrom(self, bufsize):
        '''
            first a data packet is recived that has the same wireformat as above ^^^
        '''
        self.data                #line 37   the data that is received
        self.sourceAddr          #line 83   the addresses from where the data was sent from
        self.sourcePort          #line 31 (bit 0-16)  the port number from where the data was sent from
        
        

        #recvfrom has the return format of:
        #(string,address) 
        #where string = data and address = (IP address, port number)
        return (self.data,(self.sourceAddr,self.sourcePort))     