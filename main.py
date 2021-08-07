from cpu import *

def main():
    mainCode = [
        MOV_LIT_REG,
        0x00,
        0xff,
        R1,

        

        MOV_REG_MEM,
        R1,
        0x30,
        0xce,
    ]
    
    
    
    cpu = CPU(256*256)
    

    
    cpu.load(mainCode)
    #cpu.load(subroutine, 0x3000)
    
   
    #cpu.debug()
    #cpu.viewMemoryAt(0xffff-1-42, 44)

    cpu.run()
    
        
        

if __name__ == "__main__":
    main()

