# Computer Networks Lab 6

# Elizabeth Duncan and Mary Ruthven



class Bit_structure(object):   
    def __init__(self):
        self.transmit_field_offset = 0
        self.bit_fields = []

    def getBitType(self):
        return self.bit_fields

    def register(self,arg_Bit_field_type):
        bdf_type, specified_bdf_offset = arg_Bit_field_type
        self.transmit_field_offset += specified_bdf_offset
        #self.bit_field_offset  +=  bfd_type.length
        self.bit_fields.extend(Bit_Data_Field(bdf_type,specified_bdf_offset))

class Bit_field_type(object):
    def __init__(self)      :raise NotImplemented
    def __eq__  (self,other):raise NotImplemented
    def __le__  (self,other):raise NotImplemented
    def __len__ (self)      :raise NotImplemented
    def __repr__(self)      :raise NotImplemented
    def __inv__ (self)      :raise NotImplemented
    def __or__   (self,other):raise NotImplemented
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

def Bit_Data_Field(num, length):
    binary = "{0:b}".format(num)
    array = [0 for x in range(length-len(binary))]
    for b in binary:
        array.append(b)
    return array

def Ordinal(ordinalType, length):
    if ordinalType == "Ack":
        value = 4
    return value, length





message = Bit_structure()
message.register(Ordinal("Ack", 16))
print(message.getBitType())
message.register(IntType(10, 16))
print(message.getBitType())




