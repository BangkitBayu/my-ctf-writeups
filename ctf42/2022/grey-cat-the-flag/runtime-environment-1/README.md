# Runtime Environment 1

> **Description**: GvVf+fHWz1tlOkHXUk3kz3bqh4UcFFwgDJmUDWxdDTTGzklgIJ+fXfHUh739+BUEbrmMzGoQOyDIFIz4GvTw+j--

## Overview

| Property       | Detail                                                                         |
| -------------- | ------------------------------------------------------------------------------ |
| Organizer      | GreyCatTheFlag                                                                 |
| Year           | 2022                                                                           | 
| Difficulty     | Easy 299/1000                                                                  |
| Techniques           | `#go-reversing` `#custom-base6`                                                      |
| Challenge link | [Click me](https://ctf42.online/ctfs/greycattheflag/2022/runtimeenvironment1/) |

## 1. Initial Reconnaissance

I run this program, the program request input, then program give a key

```bash
$ ./binary
tes
z1Ur
```

also, i got challenge.txt like this:

```text
GvVf+fHWz1tlOkHXUk3kz3bqh4UcFFwgDJmUDWxdDTTGzklgIJ+fXfHUh739+BUEbrmMzGoQOyDIFIz4GvTw+j--
```

Then, i tried to check `binary` program

```bash
$ file ./binary
./binary: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=OHBJFJh5S4MEkda8Q683/cMydJq6y9QbVjBCjK1KP/8R1f9ddSl9EfpM8KP2Dy/3G9-Ju3BW7WUsgoGNyvl, not stripped
```

This program, build by Go language with not stripped binary and arch x64.

Then, i check security program

```bash
$ checksec --file=./binary
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
No RELRO        No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   2827 Symbols	  No	0		0		./binary
```

**Security details**
| Property | Detail |
| -------------- | ---------------------------------------|
| No RELRO | No GOT overwrite protection|
| No canary found | No canary protection when program crashed overflow |
| NX disabled | No Protection from shellcode |
| No PIE | Static base address when program running |

## 2. Static Analysis 

I used ghidra to get pseudocode

### 2.1 main.main - entry program
```c++
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void main.main(void)

{
  int cap;
  io.Reader r;
  string s;
  string val;
  io.Writer w;
  []uint8 dst;
  []interface_{} a;
  []uint8 ~r2;
  []interface_{} a_00;
  string str;
  []uint8 src;
  error err;
  error err_00;
  []uint8 ~r2_00;
  undefined1 auVar1 [24];
  runtime._type *et;
  void *in_RBX;
  int len;
  void *extraout_RBX;
  void *~r3;
  int in_FS_OFFSET;
  int *in_stack_ffffffffffffff60;
  runtime.tmpBuf *buf;
  uint8 *x;
  runtime.itab *in_stack_ffffffffffffff80;
  runtime.tmpBuf *in_stack_ffffffffffffff88;
  undefined8 in_stack_ffffffffffffff90;
  uint8 *in_stack_ffffffffffffff98;
  uint8 local_58 [32];
  runtime.tmpBuf *local_38;
  int *local_30;
  undefined *local_28 [2];
  undefined *local_18 [2];
  
                    /* Unresolved local var: string * &src@[???]
                       Unresolved local var: []uint8 buf@[???] */
  while (local_28 <= *(undefined ***)(*(int *)(in_FS_OFFSET + -8) + 0x10)) {
    runtime.morestack_noctxt();
    in_RBX = extraout_RBX;
  }
  runtime.newobject((runtime._type *)&DAT_004ab9c0,in_RBX);
  local_18[0] = &DAT_004a86a0;
  buf = (runtime.tmpBuf *)0x1;
  x = (uint8 *)0x1;
  r.data = os.Stdin;
  r.tab = (runtime.itab *)&go.itab.*os.File,io.Reader;
  a.len = 1;
  a.array = (interface_{} *)local_18;
  a.cap = 1;
  err.data = in_stack_ffffffffffffff88;
  err.tab = in_stack_ffffffffffffff80;
  local_30 = in_stack_ffffffffffffff60;
  fmt.Fscanln(r,a,(int)in_stack_ffffffffffffff60,err);
  cap = local_30[1];
  et = (runtime._type *)
       (((SUB168(SEXT816(-0x5555555555555555) * SEXT816(cap + 2),8) + cap + 2 >> 1) -
        (cap + 2 >> 0x3f)) * 4);
  runtime.makeslice(et,len,cap,~r3);
  s.len = *local_30;
  s.str = local_58;
  ~r2.len = (int)buf;
  ~r2.array = (uint8 *)local_30[1];
  ~r2.cap = (int)x;
  local_38 = buf;
  runtime.stringtoslicebyte(buf,s,~r2);
  dst.len = (int)et;
  dst.array = *local_38;
  dst.cap = (int)et;
  src.len = (int)x;
  src.array = *buf;
  src.cap = (int)in_stack_ffffffffffffff80;
  ~r2_00.len = in_stack_ffffffffffffff90;
  ~r2_00.array = *in_stack_ffffffffffffff88;
  ~r2_00.cap = (int)in_stack_ffffffffffffff98;
  main.Encode(dst,src,~r2_00);
  auVar1._8_8_ = in_stack_ffffffffffffff90;
  auVar1._0_8_ = in_stack_ffffffffffffff88;
  auVar1._16_8_ = 0;
  str.len = (int)x;
  str.str = in_stack_ffffffffffffff98;
  runtime.slicebytetostring(in_stack_ffffffffffffff88,([]uint8)(auVar1 << 0x40),str);
  val.len = (int)in_stack_ffffffffffffff80;
  val.str = x;
  runtime.convTstring(val,x);
  local_28[0] = &DAT_004ab9c0;
  w.data = os.Stdout;
  w.tab = (runtime.itab *)&go.itab.*os.File,io.Writer;
  a_00.len = 1;
  a_00.array = (interface_{} *)local_28;
  a_00.cap = 1;
  err_00.data = in_stack_ffffffffffffff88;
  err_00.tab = in_stack_ffffffffffffff80;
  fmt.Fprintln(w,a_00,(int)local_28,err_00);
  return;
}
```

### 2.2 main.Encode - logic to make base64 custom

```c++

void main.Encode([]uint8 dst,[]uint8 src,[]uint8 ~r2)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  uint8 local_48 [64];
  
                    /* Unresolved local var: int di@[???]
                       Unresolved local var: int si@[???]
                       Unresolved local var: int n@[???]
                       Unresolved local var: int remain@[???]
                       Unresolved local var: uint val@[???] */
  local_48[0] = 'N';
  local_48[1] = 'a';
  local_48[2] = 'R';
  local_48[3] = 'v';
  local_48[4] = 'J';
  local_48[5] = 'T';
  local_48[6] = '1';
  local_48[7] = 'B';
  local_48[8] = '/';
  local_48[9] = 'm';
  local_48[10] = '6';
  local_48[0xb] = 'A';
  local_48[0xc] = 'O';
  local_48[0xd] = 'X';
  local_48[0xe] = 'L';
  local_48[0xf] = '9';
  local_48[0x10] = 'V';
  local_48[0x11] = 'D';
  local_48[0x12] = 'F';
  local_48[0x13] = 'I';
  local_48[0x14] = 'b';
  local_48[0x15] = 'U';
  local_48[0x16] = 'G';
  local_48[0x17] = 'k';
  local_48[0x18] = 'C';
  local_48[0x19] = '+';
  local_48[0x1a] = 's';
  local_48[0x1b] = 'S';
  local_48[0x1c] = 'n';
  local_48[0x1d] = 'z';
  local_48[0x1e] = 'h';
  local_48[0x1f] = '5';
  local_48[0x20] = 'j';
  local_48[0x21] = 'x';
  local_48[0x22] = 'Q';
  local_48[0x23] = '2';
  local_48[0x24] = '7';
  local_48[0x25] = '3';
  local_48[0x26] = 'd';
  local_48[0x27] = '4';
  local_48[0x28] = 'l';
  local_48[0x29] = 'H';
  local_48[0x2a] = 'P';
  local_48[0x2b] = 'g';
  local_48[0x2c] = '0';
  local_48[0x2d] = 'w';
  local_48[0x2e] = 'c';
  local_48[0x2f] = 'E';
  local_48[0x30] = 'p';
  local_48[0x31] = 'Y';
  local_48[0x32] = 'q';
  local_48[0x33] = 'r';
  local_48[0x34] = 'u';
  local_48[0x35] = 'W';
  local_48[0x36] = 'y';
  local_48[0x37] = 'f';
  local_48[0x38] = 'Z';
  local_48[0x39] = 'o';
  local_48[0x3a] = 'M';
  local_48[0x3b] = '8';
  local_48[0x3c] = 'i';
  local_48[0x3d] = 't';
  local_48[0x3e] = 'K';
  local_48[0x3f] = 'e';
  uVar2 = 0;
  uVar3 = 0;
  while( true ) {
    if (((SUB168(SEXT816(-0x5555555555555555) * SEXT816(src.len),8) + src.len >> 1) -
        (src.len >> 0x3f)) * 3 <= (int)uVar2) {
      iVar4 = src.len - uVar2;
      if (src.len == uVar2) {
        return;
      }
      if ((uint)src.len <= uVar2) {
                    /* WARNING: Subroutine does not return */
        runtime.panicIndex();
      }
      uVar5 = (uint)src.array[uVar2] << 0x10;
      if (iVar4 == 2) {
        if ((uint)src.len <= uVar2 + 1) {
                    /* WARNING: Subroutine does not return */
          runtime.panicIndex();
        }
        uVar5 = (uint)src.array[uVar2 + 1] << 8 | uVar5;
      }
      if ((uint)dst.len <= uVar3) {
                    /* WARNING: Subroutine does not return */
        runtime.panicIndex();
      }
      dst.array[uVar3] = local_48[uVar5 >> 0x12];
      if ((uint)dst.len <= uVar3 + 1) {
                    /* WARNING: Subroutine does not return */
        runtime.panicIndex();
      }
      dst.array[uVar3 + 1] = local_48[uVar5 >> 0xc & 0x3f];
      if (iVar4 == 1) {
        if ((uint)dst.len <= uVar3 + 2) {
                    /* WARNING: Subroutine does not return */
          runtime.panicIndex();
        }
        dst.array[uVar3 + 2] = 0x2d;
        if ((uint)dst.len <= uVar3 + 3) {
                    /* WARNING: Subroutine does not return */
          runtime.panicIndex();
        }
        dst.array[uVar3 + 3] = 0x2d;
      }
      else if (iVar4 == 2) {
        if ((uint)dst.len <= uVar3 + 2) {
                    /* WARNING: Subroutine does not return */
          runtime.panicIndex();
        }
        dst.array[uVar3 + 2] = local_48[uVar5 >> 6 & 0x3f];
        if ((uint)dst.len <= uVar3 + 3) {
                    /* WARNING: Subroutine does not return */
          runtime.panicIndex();
        }
        dst.array[uVar3 + 3] = 0x2d;
      }
      return;
    }
    if ((uint)src.len <= uVar2) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
    if ((uint)src.len <= uVar2 + 1) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
    uVar5 = (uint)src.array[uVar2 + 1] << 8 | (uint)src.array[uVar2] << 0x10;
    if ((uint)src.len <= uVar2 + 2) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
    bVar1 = src.array[uVar2 + 2];
    if ((uint)dst.len <= uVar3) break;
    dst.array[uVar3] = local_48[src.array[uVar2] >> 2];
    if ((uint)dst.len <= uVar3 + 1) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
    dst.array[uVar3 + 1] = local_48[uVar5 >> 0xc & 0x3f];
    if ((uint)dst.len <= uVar3 + 2) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
    dst.array[uVar3 + 2] = local_48[(bVar1 | uVar5) >> 6 & 0x3f];
    if ((uint)dst.len <= uVar3 + 3) {
                    /* WARNING: Subroutine does not return */
      runtime.panicIndex();
    }
                    /* Unresolved local var: uint val@[???] */
    dst.array[uVar3 + 3] = local_48[bVar1 & 0x3f];
    uVar2 = uVar2 + 3;
    uVar3 = uVar3 + 4;
  }
                    /* WARNING: Subroutine does not return */
  runtime.panicIndex();
}
```

## 3. Dynamic Analysis

I used gdb + pwndbg to do dynamic analysis:

I set breakpint in `*main.main`, program requested input when

```bash
0x49988f <main.main+47>     lea    rax, [rip + 0x1212a]            RAX => 0x4ab9c0 (type.*+72128) ◂— 0x10
   0x499896 <main.main+54>     mov    qword ptr [rsp], rax            [0xc0000c4eb0] <= 0x4ab9c0 (type.*+72128) ◂— 0x10
   0x49989a <main.main+58>     call   runtime[newobject]          <runtime[newobject]>
 
   0x49989f <main.main+63>     mov    rax, qword ptr [rsp + 8]
   0x4998a4 <main.main+68>     mov    qword ptr [rsp + 0x78], rax
 ► 0x4998a9 <main.main+73>     xorps  xmm0, xmm0

```

Then, enter `tes`, next `tes` to be argumen into main.Encode function

```bash
0x49999e <main.main+318>    call   main[Encode]                <main[Encode]>
        rdi: 0xc0000c0f00 ◂— 0x736574 /* 'tes' */
        rsi: 3
        rdx: 0xc0000120e0 ◂— 0x736574 /* 'tes' */
        rcx: 0x73
```

After that, `tes` encoded by base64 custom encoding

```bash
0x499694 <main[Encode]+340>    mov    rdx, rbx     RDX => 3
   0x499697 <main[Encode]+343>    sub    rbx, rax     RBX => 0 (3 - 3)
 ► 0x49969a <main[Encode]+346>    test   rbx, rbx     0 & 0     EFLAGS => 0x246 [ cf PF af ZF sf IF df of iopl:00 ac ]
   0x49969d <main[Encode]+349>  ✔ je     main[Encode]+609            <main[Encode]+609>
    ↓
   0x4997a1 <main[Encode]+609>    mov    qword ptr [rsp + 0x90], rsi     [0xc0000c0ee0] <= 0xc0000120e4 ◂— 0x7255317a /* 'z1Ur' */
   0x4997a9 <main[Encode]+617>    mov    qword ptr [rsp + 0x98], rdi     [0xc0000c0ee8] <= 4
   0x4997b1 <main[Encode]+625>    mov    rax, qword ptr [rsp + 0x70]     RAX, [0xc0000c0ec0] => 4
   0x4997b6 <main[Encode]+630>    mov    qword ptr [rsp + 0xa0], rax     [0xc0000c0ef0] <= 4

```

## 4. Solution
I build solver script to completed this challenge, why i use 5 times decoded? because i tried to once decoded but don't get plaintext

```python
c = "GvVf+fHWz1tlOkHXUk3kz3bqh4UcFFwgDJmUDWxdDTTGzklgIJ+fXfHUh739+BUEbrmMzGoQOyDIFIz4GvTw+j--"

alphabet = "NaRvJT1B/m6AOXL9VDFIbUGkC+sSnzh5jxQ273d4lHPg0wcEpYqruWyfZoM8itKe"

reverse_alphabet = {}

for index,char in enumerate(alphabet):
  reverse_alphabet[char] = index

def decoded(c):
    result = b""

    # Proses ciphertext per 4 karakter
    for i in range(0, len(c), 4):
        block = c[i:i+4]

        padding = block.count("-")
        values = []

        for char in block.rstrip("-"):
            values.append(reverse_alphabet[char])

        while len(values) < 4:
            values.append(0)

        combined = (
            (values[0] << 18) |
            (values[1] << 12) |
            (values[2] << 6) |
            values[3]
        )

        byte1 = (combined >> 16) & 0xFF
        byte2 = (combined >> 8) & 0xFF
        byte3 = combined & 0xFF

        if padding == 0:
            result += bytes([byte1, byte2, byte3])
        elif padding == 1:
            result += bytes([byte1, byte2])
        elif padding == 2:
            result += bytes([byte1])

    return result


current = c

for i in range(1, 5): 
  current = decoded(current).decode("ascii")
  
  print(f"[{i}/5]: {current}")
```

**Flag**: grey{B4s3d_G0Ph3r_r333333}

