
class Memory:
    def __init__(self, sizeInBytes):
        self.array = bytearray(sizeInBytes)
    
    def get(self, address):
        return self.array[address]
    
    def get16(self, address):
        return (self.array[address] << 8) + self.array[address+1]

    def set(self, address, value):
        self.array[address] = value
    
    def set16(self, address, value):
        self.array[address] = value >> 8
        self.array[address+1] = value - (self.array[address] << 8)



