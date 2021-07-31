from instructionSet import *
from memory import Memory

class CPU:
    def __init__(self, memorySize):
        self.memory = Memory(memorySize)

        self.registerNames = {"ip": 0x00, "acc": 0x02, "r1": 0x04, 
                              "r2": 0x06, "r3": 0x08, "r4": 0x0a}

        self.registers = Memory(len(self.registerNames) * 2)

    def getRegister(self, name):
        return self.registers.get16(self.registerNames[name])
    
    def setRegister(self, name, value):
        self.registers.set16(self.registerNames[name], value)

    def fetch(self):
        instructionAdress = self.getRegister("ip")
        instruction = self.memory.get(instructionAdress)
        self.setRegister("ip", instructionAdress+1)
        return instruction
    
    def fetch16(self):
        instructionAdress = self.getRegister("ip")
        instruction = self.memory.get16(instructionAdress)
        self.setRegister("ip", instructionAdress+2)
        return instruction

    def execute(self, instruction):
        
        if instruction == MOV_LIT_REG:
            literal = self.fetch16()
            registerAddress = (self.fetch() % len(self.registerNames)) * 2
            self.registers.set16(registerAddress, literal)
        
        elif instruction == MOV_REG_REG:
            registerFrom = (self.fetch() % len(self.registerNames)) * 2
            registerTo = (self.fetch() % len(self.registerNames)) * 2
            value = self.registers.get16(registerFrom)

            self.registers.set16(registerTo, value)
        

        
        elif instruction == MOV_REG_MEM:
            registerAddress = (self.fetch() % len(self.registerNames)) * 2
            memoryAddress = self.fetch16() 
            value = self.registers.get16(registerAddress)
            
            self.memory.set16(memoryAddress, value)
        
        elif instruction == MOV_MEM_REG:
            memoryAddress = self.fetch16() 
            registerAddress = (self.fetch() % len(self.registerNames)) * 2
            value = self.memory.get16(memoryAddress)
            
            self.registers.set16(registerAddress, value)
        
        elif instruction == MOV_MEM_MEM:
            pass

        elif instruction == ADD_REG_REG:
            r1 = self.fetch()
            r2 = self.fetch()

            registerValue1 = self.registers.get16(r1*2)
            registerValue2 = self.registers.get16(r2*2)

            self.setRegister("acc", registerValue1 + registerValue2)
        
        elif instruction == JMP_N_EQ:
            value = self.fetch16()
            address = self.fetch16()

            if value != self.getRegister("acc"):
                self.setRegister("ip", address)


    def step(self):
        instruction = self.fetch()
        return self.execute(instruction)
    
    def debug(self):
        for name in self.registerNames:
            print("{}: 0x{:04X}".format(name, self.getRegister(name)))
            pass

    def viewMemoryAt(self, address):
        print("0x{:04X}:".format(address), end="")
        for ad in range(address, address + 8):
            print(" 0x{:04X}".format(self.memory.get(ad)), end="")
        print("")
    
    def load(self, code):
        for i in range(len(code)):
            self.memory.set(i, code[i])
        


