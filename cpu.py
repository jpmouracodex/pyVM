from instructionSet import *
from memory import Memory
import pygame

class CPU:
    def __init__(self, memorySize):
        self.memory = Memory(memorySize)

        self.registerNames = {"ip": 0x00, "acc": 0x02, "r1": 0x04, 
                              "r2": 0x06, "r3": 0x08, "r4": 0x0a,
                              "r5": 0x0c, "r6": 0x0e, "r7": 0x10,
                              "r8": 0x12, "sp": 0x14, "fp": 0x16
                              }

        self.registers = Memory(len(self.registerNames) * 2)

        self.setRegister("sp", 0xffff - 1)
        self.setRegister("fp", 0xffff - 1)

        self.stackFrameSize = 0

        pygame.init()
        self.screen = pygame.display.set_mode((256, 256))
        pygame.display.set_caption('pyVM') 

    def getRegister(self, name):
        return self.registers.get16(self.registerNames[name])

    def setRegister(self, name, value):
        self.registers.set16(self.registerNames[name], value)

    def getRegisterIndex(self):
        return (self.fetch() % len(self.registerNames)) * 2

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

    def push(self, value):
        spAddress = self.getRegister("sp")
        self.memory.set16(spAddress, value)
        self.setRegister("sp", spAddress - 2)
        self.stackFrameSize += 2

    def pop(self):
        nextSpAddress = self.getRegister("sp") + 2
        self.setRegister("sp", nextSpAddress)
        return self.memory.get16(nextSpAddress)
        self.stackFrameSize -= 2

    def pushState(self):
        self.push(self.getRegister("r1"))
        self.push(self.getRegister("r2"))
        self.push(self.getRegister("r3"))
        self.push(self.getRegister("r4"))
        self.push(self.getRegister("r5"))
        self.push(self.getRegister("r6"))
        self.push(self.getRegister("r7"))
        self.push(self.getRegister("r8"))
        self.push(self.getRegister("ip"))

        self.push(self.stackFrameSize + 2)
        self.setRegister("fp", self.getRegister("sp"))
        self.stackFrameSize = 0

    def popState(self):
        framePointerAddress = self.getRegister("fp")
        self.setRegister("sp", framePointerAddress)

        self.stackFrameSize = self.pop()
        stackFrameSize = self.stackFrameSize

        self.setRegister("ip", self.pop())
        self.setRegister("r8", self.pop())
        self.setRegister("r7", self.pop())
        self.setRegister("r6", self.pop())
        self.setRegister("r5", self.pop())
        self.setRegister("r4", self.pop())
        self.setRegister("r3", self.pop())
        self.setRegister("r2", self.pop())
        self.setRegister("r1", self.pop())
        
        nArgs = self.pop()
        for i in range(nArgs):
            self.pop()
        
        self.setRegister("fp", framePointerAddress + stackFrameSize)

    def execute(self, instruction):
        
        if instruction == MOV_LIT_REG:
            literal = self.fetch16()
            registerAddress = self.getRegisterIndex()
            self.registers.set16(registerAddress, literal)
        
        elif instruction == MOV_REG_REG:
            registerFrom = self.getRegisterIndex()
            registerTo = self.getRegisterIndex()
            value = self.registers.get16(registerFrom)

            self.registers.set16(registerTo, value)
        
        elif instruction == MOV_REG_MEM:
            registerAddress = self.getRegisterIndex()
            memoryAddress = self.fetch16() 
            value = self.registers.get16(registerAddress)
            
            self.memory.set16(memoryAddress, value)
        
        elif instruction == MOV_MEM_REG:
            memoryAddress = self.fetch16() 
            registerAddress = self.getRegisterIndex()
            value = self.memory.get16(memoryAddress)
            
            self.registers.set16(registerAddress, value)
        
        elif instruction == ADD_REG_REG:
            r1 = self.getRegisterIndex()
            r2 = self.getRegisterIndex()

            registerValue1 = self.registers.get16(r1)
            registerValue2 = self.registers.get16(r2)

            self.setRegister("acc", registerValue1 + registerValue2)
        
        elif instruction == JMP_N_EQ:
            value = self.fetch16()
            address = self.fetch16()

            if value != self.getRegister("acc"):
                self.setRegister("ip", address)

        elif instruction == PSH_LIT:
            value = self.fetch16()
            self.push(value)
        
        elif instruction == PSH_REG:
            registerIndex = self.getRegisterIndex()
            self.push(self.registers.get16(registerIndex))

        elif instruction == POP:
            registerIndex = self.getRegisterIndex()
            value = self.pop()
            self.registers.set16(registerIndex, value)
        
        elif instruction == CAL_LIT:
            address = self.fetch16()
            self.pushState()
            self.setRegister("ip", address)

        elif instruction == CAL_LIT:
            registerIndex = self.fetch16()
            address = self.registers.get16(registerIndex)
            self.pushState()
            self.setRegister("ip", address)

        elif instruction == RET:
            self.popState()

        elif instruction == HLT:
            return True

    def step(self):
        instruction = self.fetch()
        return self.execute(instruction)
    
    def debug(self):

        for name in self.registerNames:
            print("{}: 0x{:04X}".format(name, self.getRegister(name)))
           
    def viewMemoryAt(self, address, len=8):
        print("0x{:04X}:".format(address), end="")
        for ad in range(address, address + len):
            print(" 0x{:02X}".format(self.memory.get(ad)), end="")
        print("")
    
    def load(self, code, start = 0x00):
        code = bytearray(code)
        address = start
        for byte in code:
            self.memory.set(address, byte)
            address += 1

    def drawScreen(self):
        self.screen.fill((0,0,0))
        for address in range(0x3000, 0x30ff):
            value = self.memory.get(address)
            address -= 0x3000 + 1 
            x = address % 16
            y = address // 16
            pygame.draw.rect(self.screen, 
            (value, value, value),
            pygame.Rect(x*16, y*16, x*16+16, y*16+16))

        pygame.display.update()
        

    def run(self):
        halt = False

        while not halt:
            halt = self.step()
            self.drawScreen()