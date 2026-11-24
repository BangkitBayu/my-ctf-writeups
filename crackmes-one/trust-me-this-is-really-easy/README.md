# trust me this is really easy :)

> **Description**:This is a Linux x64 crackme written in C++. It features a basic anti-debugging protection (ptrace) and an obfuscated validation routine.Your goal: Find the correct password to reveal the flag. Hint: If you get stuck, try bypassing the anti-debugger first to properly analyze the loop logic. Good luck!"

## Overview

| Property       | Detail                                                            |
| -------------- | ----------------------------------------------------------------- |
| Author         | vetementsvmnts                                                    |
| Platform       | Unix/linux etc.                                                   |
| Language       | C/C++                                                             |
| Difficulty     | 1.0                                                               |
| Arch           | x86-64                                                            |
| Challenge link | [Click me](https://crackmes.one/crackme/6ab2c094c2d73ca6ae44d7f6) |

## Initial Reconnaissance

First, i checking file program like this:

```bash
$ file ./crackme

./crackme: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d430158416125d07d254c6403c3b25073201ff55, for GNU/Linux 3.2.0, not stripped
```

Second, i checking program security like this:

```bash
$ checksec --file=./crackme

RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   79 Symbols	  No	0		0		./crackme
```

**Security details**
| Property | Detail |
| -------------- | ---------------------------------------|
| Partial RELRO | GOT overwrite protection|
| No canary found | No canary protection when program crashed overflow |
| NX enabled | Protection from shellcode |
| PIE enabled | Dynamic base address when program running |

Third, i checking all strings which program output, i got this:

```bash
$ strings ./crackme

Debugger detected. Exiting.
Enter the password: 
Access Denied.
CMO{ilovecrackmes}
```

## Solution

I got the flag when i tried to showing program string with `strings` command.

```text
CMO{ilovecrackmes}
```