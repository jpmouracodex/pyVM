from cpu import *

def main():
    mainCode = [
        PSH_LIT,
        0x33,
        0x33,
        
        PSH_LIT,
        0x22,
        0x22,
        
        MOV_LIT_REG,
        0x12,
        0x34,
        R1,

        MOV_LIT_REG,
        0x56,
        0x78,
        R2,

        PSH_LIT,
        0x00,
        0x00,

        CAL_LIT,
        0x30,
        0x00,

        PSH_LIT,
        0x44,
        0x44,
    ]
    
    subroutine = [
        PSH_LIT,
        0x01,
        0x02,

        PSH_LIT,
        0x03,
        0x04,

        PSH_LIT,
        0x05,
        0x06,

        MOV_LIT_REG,
        0x07,
        0x08,
        R1,

        MOV_LIT_REG,
        0x09,
        0x0a,
        R2,
        
        RET

    ]
    
    cpu = CPU(256*256)

    
    cpu.load(mainCode)
    cpu.load(subroutine, 0x3000)
    
    while True:
        cpu.debug()
        cpu.viewMemoryAt(0xffff-1-42, 44)

        cpu.step()
        
        input()

if __name__ == "__main__":
    main()

