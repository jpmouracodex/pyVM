from cpu import *


def main():
    code = [
        MOV_MEM_REG,
        0x01,
        0x00,
        R1,

        MOV_LIT_REG,
        0x00,
        0x01,
        R2,

        ADD_REG_REG,
        R1,
        R2,


        MOV_REG_MEM,
        ACC,
        0x01,
        0x00,

        JMP_N_EQ,
        0x00,
        0x03,
        0x00,
        0x00
    ]

    code = bytearray(code)
    cpu = CPU(256*256)
    
    cpu.load(code)
    
    while True:
        cpu.step()
        cpu.debug()
        
        cpu.viewMemoryAt(0x0100)
        input()

if __name__ == "__main__":
    main()

