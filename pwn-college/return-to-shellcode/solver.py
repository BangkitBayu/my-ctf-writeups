from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

# File executable target

exe = "./chall" 
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "debug"

# ==========================================
# CONNECTION
# ==========================================

process(BINARY)


# ==========================================
# EXPLOIT / SOLVER
# ==========================================

def exploit(io):
    
    """
    Function to run exploitation
    
    Writing your exploitation logic steps in here
    
    Parameter:
    io: connection
    """


# ==========================================
# MAIN
# ==========================================

def main():

    io = start()

    exploit(io)
    
    io.interactive()


if __name__ == "__main__":
    main()
