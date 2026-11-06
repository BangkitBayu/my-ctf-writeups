# Registers

> **Description**: The program keeps one number, changes it in four steps, and asks you for the final result. Read the steps in the program's assembly, do the math yourself, and type the answer in hex.

| Property           | Detail                                                                                                     |
| :----------------- | :--------------------------------------------------------------------------------------------------------- |
| **Category**       | Reverse engineering                                                                                        |
| **Challenge URL**  | [https://pwn.college/intro-re-pwn~5933fc84/assembly/](https://pwn.college/intro-re-pwn~5933fc84/assembly/) |
| **Status**         | In progress                                                                                                |
| **Date Completed** |                                                                                                            |

## Analysis

**File & Checksec**

```
/challenge/registers: setuid ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=48f69c9f60f780a1ad120c885c9559e1bbfe585f, for GNU/Linux 3.2.0, not stripped

Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
```

Diberikan file README.md berikut:

<details>
<summary>README.md</summary>
# registers

## Background

When a program runs, the CPU does its math in tiny, very fast storage slots called **registers**. A register holds one number at a time. Programs are made of **instructions**, which are single small commands such as "add this to that". **Assembly** is the readable text form of those instructions. A **disassembler** (`objdump`) turns a compiled program back into assembly so you can read it.

Numbers in assembly are usually written in **hex** (base 16: digits `0-9` then `a-f`, with `0x` in front). A number written directly inside an instruction, like the `0x64` in `add eax,0x64`, is called an **immediate**.

For this challenge you need four instructions and one idea:

- `mov`, `add`, `sub`, `shl` and `xor` (module lesson page 3, "The core instructions").
- Intel syntax puts the destination first: `add eax, 0x10` means `eax = eax + 0x10` (page 1).
- `DWORD PTR [rbp-0x4]` means "the 4-byte value stored 4 bytes below the address in `rbp`", which is where `-O0` code keeps a local variable (page 5).

If any of those words are new, read lesson pages 1 to 3 of this module first. The worked example on page 9 walks through code shaped like this one line by line.

## How to start

```

/challenge/registers
objdump -d -M intel --disassemble=main /challenge/registers

```

The first command runs the program so you see what it asks. The second prints only the `main` function in Intel style. (`objdump -d -M intel /challenge/registers | more` shows the whole program a screen at a time; Space for more, `q` to quit.)

## The challenge

`/challenge/registers` starts with a number, then applies four operations to it: an add, a left shift, an xor, and a subtract. It asks you for the final number, in hex without a `0x` in front. If you type the right value, it prints the flag.

You never see the starting number or the operation values unless you read the assembly.

## Hints (open one at a time, stop as soon as you can continue)

1. Only read inside `main`. The first few calls in it (`geteuid`, `setreuid`, `printf`, `fflush`, `scanf`) are setup and reading your input; the part you want comes after `scanf`.
2. After the input is read, look for a short run of lines that all touch the same stack slot, written `DWORD PTR [rbp-0x..]`, and each end in a hex number (a shift by 1 may show a plain `1` instead of `0x1`).
3. The first of those lines (`mov`) stores the starting value. The next lines are the operations, in the order the program runs them: `add` adds, `shl` shifts bits left (shifting left by N multiplies by 2 to the power N), `xor` flips bits, `sub` subtracts.
4. Do the operations in the same order in Python (`python3`, then `hex(...)`). The program uses 32-bit numbers, so keep only the lowest 32 bits: `& 0xffffffff`. Type the result without the `0x`.
</details>

Berdasarkan deskripsi soal yang diberikan, program memiliki 1 angka yang akan diubah dalam 4 steps, lalu saya melakukan analisis lebih dalam

### 1. Disassemble fungsi main

```bash
objdump -d -M intel --disassemble=main /challenge/registers
```

Output

```
  4012ef:       f3 0f 1e fa             endbr64
  4012f3:       55                      push   rbp
  4012f4:       48 89 e5                mov    rbp,rsp
  4012f7:       48 83 ec 10             sub    rsp,0x10
  4012fb:       e8 20 fe ff ff          call   401120 <geteuid@plt>
  401300:       be ff ff ff ff          mov    esi,0xffffffff
  401305:       89 c7                   mov    edi,eax
  401307:       e8 44 fe ff ff          call   401150 <setreuid@plt>
  40130c:       bf 20 20 40 00          mov    edi,0x402020
  401311:       b8 00 00 00 00          mov    eax,0x0
  401316:       e8 e5 fd ff ff          call   401100 <printf@plt>
  40131b:       48 8b 05 46 2d 00 00    mov    rax,QWORD PTR [rip+0x2d46]        # 404068 <stdout@GLIBC_2.2.5>
  401322:       48 89 c7                mov    rdi,rax
  401325:       e8 16 fe ff ff          call   401140 <fflush@plt>
  40132a:       48 8d 45 f8             lea    rax,[rbp-0x8]
  40132e:       48 89 c6                mov    rsi,rax
  401331:       bf 3f 20 40 00          mov    edi,0x40203f
  401336:       b8 00 00 00 00          mov    eax,0x0
  40133b:       e8 40 fe ff ff          call   401180 <__isoc99_scanf@plt>
  401340:       83 f8 01                cmp    eax,0x1
  401343:       74 11                   je     401356 <main+0x67>
  401345:       bf 48 20 40 00          mov    edi,0x402048
  40134a:       e8 91 fd ff ff          call   4010e0 <puts@plt>
  40134f:       b8 01 00 00 00          mov    eax,0x1
  401354:       eb 3d                   jmp    401393 <main+0xa4>
  401356:       c7 45 fc 09 5e 00 00    mov    DWORD PTR [rbp-0x4],0x5e09
  40135d:       81 45 fc 04 1f 00 00    add    DWORD PTR [rbp-0x4],0x1f04
  401364:       d1 65 fc                shl    DWORD PTR [rbp-0x4],1
  401367:       81 75 fc d2 a7 00 00    xor    DWORD PTR [rbp-0x4],0xa7d2
  40136e:       81 6d fc 3d 2c 00 00    sub    DWORD PTR [rbp-0x4],0x2c3d
  401375:       8b 45 f8                mov    eax,DWORD PTR [rbp-0x8]
  401378:       39 45 fc                cmp    DWORD PTR [rbp-0x4],eax
  40137b:       75 07                   jne    401384 <main+0x95>
  40137d:       e8 f4 fe ff ff          call   401276 <print_flag>
  401382:       eb 0a                   jmp    40138e <main+0x9f>
  401384:       bf 70 20 40 00          mov    edi,0x402070
  401389:       e8 52 fd ff ff          call   4010e0 <puts@plt>
  40138e:       b8 00 00 00 00          mov    eax,0x0
  401393:       c9                      leave
  401394:       c3                      ret
```

Dari petunjuk yang diberikan kita hanya perlu fokus pada operasi setelah pemanggilan fungsi scanf yaitu:

```
  401356:       c7 45 fc 09 5e 00 00    mov    DWORD PTR [rbp-0x4],0x5e09
  40135d:       81 45 fc 04 1f 00 00    add    DWORD PTR [rbp-0x4],0x1f04
  401364:       d1 65 fc                shl    DWORD PTR [rbp-0x4],1
  401367:       81 75 fc d2 a7 00 00    xor    DWORD PTR [rbp-0x4],0xa7d2
  40136e:       81 6d fc 3d 2c 00 00    sub    DWORD PTR [rbp-0x4],0x2c3d
```

maksud dari instruksi berikut yaitu

1. MOV - menyiapkan variabel 0x5e09
2. ADD - Melakukan penjumlahan dengan 0x1f04
3. SHL - Melakukan pergeseran ke kiri sebesar 1
4. XOR - Melakukan XOR dengan 0xa7d2
5. SUB - Melakukan pengurangan dengan 0x2c3d

## Exploitation

Saya susun kalkulator berikut

```python
val = 0x5e09
val += 0x1f04
val <<= 1
val ^= 0xa7d2
val -= 0x2c3d

# Atur batas ke 32 bit karena DWORD PTR [rbp-0x4]
val &= 0xffffffff
print(hex(val))
```

## New Knowledge

- Mempelajari register
- Memahami alur instruksi pada assembly x86-64

## References

- [https://pwn.college/intro-re-pwn~5933fc84/assembly/](https://pwn.college/intro-re-pwn~5933fc84/assembly/)
