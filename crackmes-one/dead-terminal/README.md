# Dead Terminal

> **Description**: You found an abandoned shell. Most commands behave exactly as expected—but something else is buried inside it. There is a command you were never told about, and it is waiting for the right key. Your objective is simple: discover what the shell is hiding and recover the valid input.

## Overview

| Property       | Detail                                                            |
| -------------- | ----------------------------------------------------------------- |
| Author         | soulreaper                                                        |
| Platform       | Unix/linux etc.                                                   |
| Language       | C/C++                                                             |
| Difficulty     | 2.0                                                               |
| Arch           | x86-64                                                            |
| Challenge link | [Click me](https://crackmes.one/crackme/6a77c5d1df981859694944b8) |

## 1. Initial Reconnaissance

First, i checking file program like this:

```bash
$ file ./soulreaper_shell

./soulreaper_shell: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=74e39e9b70f9bb11332dec6fa87a89474089d670, for GNU/Linux 3.2.0, stripped
```

Second, i checking program security like this:

```bash
$ checksec --file=./soulreaper_shell

RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   No Symbols	  Yes	1		2		./soulreaper_shell
```

**Security details**
| Property | Detail |
| -------------- | ---------------------------------------|
| Full RELRO | GOT overwrite protection|
| Canary found | Canary protection when program crashed overflow |
| NX enabled | Protection from shellcode |
| PIE enabled | Dynamic base address when program running |

Third, i got .rodata like this:

```bash
$ readelf -p .rodata soulreaper_shell

String dump of section '.rodata':
  [     4]  /proc/self/status
  [    16]  TracerPid:
  [    21]  Debugger Detected
  [    33]  soulreaper shell >
  [    48]  reap
  [    4d]  Usage : reap <key>
  [    61]  Access granted \n

  [    73]  Access denied
  [    82]  execvp error
  [    8f]  fork
  [    94]  exit
  [    a0]  join us : https://t.me/+blTRfHi8oKJiN2E0
```

## 2. Static Analysis

### 2.1 execvp (0x00101270) - main program

```c++
undefined4 UndefinedFunction_00101270(void)

{
  long lVar1;
  int iVar2;
  __pid_t __pid;
  char *pcVar3;
  size_t sVar4;
  long lVar5;
  undefined4 uVar6;
  long in_FS_OFFSET;
  char *apcStack_640 [65];
  char acStack_438 [1032];
  long lStack_30;

  lStack_30 = *(long *)(in_FS_OFFSET + 0x28);
  apcStack_640[0] = (char *)0x1012a1;
  iVar2 = FUN_00101610();
  if (iVar2 == 0) {
    while( true ) {
      apcStack_640[0] = (char *)0x1012c3;
      __printf_chk(2,"soulreaper shell >");
      apcStack_640[0] = (char *)0x1012cf;
      fflush(stdout);
      apcStack_640[0] = (char *)0x1012e3;
      pcVar3 = fgets(acStack_438,0x400,stdin);
      uVar6 = 0;
      if (pcVar3 == (char *)0x0) break;
      apcStack_640[0] = (char *)0x1012fb;
      sVar4 = strcspn(acStack_438,"\n");
      acStack_438[sVar4] = '\0';
      apcStack_640[0] = (char *)0x101312;
      pcVar3 = strtok(acStack_438," ");
      if (pcVar3 == (char *)0x0) {
        apcStack_640[1] = (char *)0x0;
      }
      else {
        lVar1 = 1;
        do {
          lVar5 = lVar1;
          apcStack_640[lVar5] = pcVar3;
          apcStack_640[0] = (char *)0x101333;
          pcVar3 = strtok((char *)0x0," ");
          lVar1 = lVar5 + 1;
        } while (pcVar3 != (char *)0x0 && lVar5 != 0x3f);
        apcStack_640[(long)(int)lVar5 + 1] = (char *)0x0;
        apcStack_640[0] = (char *)0x101366;
        iVar2 = strcmp(apcStack_640[1],"exit");
        if (iVar2 == 0) break;
        apcStack_640[0] = (char *)0x10137e;
        iVar2 = strcmp(apcStack_640[1],"reap");
        if (iVar2 == 0) {
          if (apcStack_640[2] == (char *)0x0) {
            apcStack_640[0] = (char *)0x101452;
            puts("Usage : reap <key> ");
          }
          else {
            apcStack_640[0] = (char *)0x101395;
            iVar2 = FUN_00101560();
            if (iVar2 == 0) {
              apcStack_640[0] = (char *)0x101404;
              puts("Access denied ");
            }
            else {
              apcStack_640[0] = (char *)0x1013ac;
              __printf_chk(2,"Access granted \n ");
              apcStack_640[0] = (char *)0x1013b8;
              puts("join us : https://t.me/+blTRfHi8oKJiN2E0");
            }
          }
        }
        else {
          apcStack_640[0] = (char *)0x1013d5;
          __pid = fork();
          if (__pid == 0) {
            apcStack_640[0] = (char *)0x10125d;
            execvp(apcStack_640[1],apcStack_640 + 1);
            apcStack_640[0] = (char *)0x101269;
            perror("execvp error");
            goto LAB_0010141c;
          }
          if (__pid < 1) {
            apcStack_640[0] = (char *)0x10124c;
            perror("fork");
          }
          else {
            apcStack_640[0] = (char *)0x1013ee;
            waitpid(__pid,(int *)0x0,0);
          }
        }
      }
    }
  }
  else {
    apcStack_640[0] = (char *)0x10141c;
    __printf_chk(2,"Debugger Detected");
LAB_0010141c:
    uVar6 = 1;
  }
  if (lStack_30 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    apcStack_640[0] = "\x0f\x1f@";
    __stack_chk_fail();
  }
  return uVar6;
}
```

### 2.2 FUN_00101560 - generate reap key

```c++
undefined8 FUN_00101560(byte *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  char *pcVar3;
  char cVar4;
  long in_FS_OFFSET;
  char local_18 [8];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_18[0] = '\x7f';
  local_18[1] = 'y';
  local_18[2] = 'x';
  local_18[3] = -0x76;
  local_18[4] = -0x7e;
  local_18[5] = -0x72;
  local_18[6] = '7';
  local_18[7] = '4';
  sVar1 = strlen((char *)param_1);
  pcVar3 = local_18;
  uVar2 = 0;
  if (sVar1 == 8) {
    cVar4 = '\a';
    do {
      if (*pcVar3 != (byte)((*param_1 ^ 0x2a) + cVar4)) {
        uVar2 = 0;
        goto LAB_001015e1;
      }
      cVar4 = cVar4 + '\x03';
      param_1 = param_1 + 1;
      pcVar3 = pcVar3 + 1;
    } while (cVar4 != '\x1f');
    uVar2 = 1;
  }
LAB_001015e1:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```

## 3. Solution

I solved this challenge using crafted payload like this:

### 3.1 Final Payload

```python
from pwn import *

exe = "./soulreaper_shell"
elf = ELF(exe)
context.binary = elf
context.arch = elf.arch
context.log_level = "notset"

io = process(exe)

def decrypt():
    msg = ""

    target_bytes = [0x7f, 0x79, 0x78, 0x8a, 0x82, 0x8e, 0x37, 0x34]

    xor_key = 0x2a

    # Initial value cVar4 = a
    x = 7

    increment = 3

    for i in range(8):
        byte = (target_bytes[i] - x) ^ xor_key
        msg += chr(byte)
        x += increment


    return msg

def exploit(io):
    password = decrypt()

    io.sendline("reap " + password)

    res = io.recv(timeout=2)
    print(res)


def main():
    exploit(io)

    io.interactive()


if __name__ == "__main__":
    main()
```
