from pwn import *

exe = "./soulreaper_shell"
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "notset"

io = process(exe)

def decrypt():
    msg = ""

    target_bytes = [0x7f, 0x79, 0x78, 0x8a, 0x82, 0x8e, 0x37, 0x34]

    xor_key = 0x2a

    # Initial value cVar4 = a
    x = 7

    increment = 3

    for i in range(8):
        byte = (target_bytes[i] - x) ^ xor_key
        msg += chr(byte)
        x += increment

    
    return msg

def exploit(io):
    password = decrypt()

    io.sendline("reap " + password)

    res = io.recv(timeout=2)
    print(res)


def main():
    exploit(io)

    io.interactive()


if __name__ == "__main__":
    main()
