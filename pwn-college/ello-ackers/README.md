# Ello Ackers!

| Property | Detail |
| :--- | :--- |
| **Category** | Pwn / Binary Exploitation |
| **Vuln** | Shellcode Injection |
| **Challenge URL** | [https://pwn.college/program-security/program-security/](https://pwn.college/program-security/program-security/) |
| **Status** | In progress |
| **Date Completed** | YYYY-MM-DD |

## Analysis

**File & Checksec**

```bash
ello-ackers: setuid ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=90260c3a772d611bbe64b23f8797b70cd13f95db, for GNU/Linux 3.2.0, not stripped

Arch:       amd64-64-little
    RELRO:      Full RELRO 
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
``` 

## Exploitation

## New Knowledge

## References
