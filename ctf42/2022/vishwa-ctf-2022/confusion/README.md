# Confusion

> **Description**: Why is everything so Confusing in here? It is not difficult to bypass the anti-debugger but find the key, to get started, here's the Username: nLYTCmdXobFRhs you'll have to use your neurons. Flag Format: vishwaCTF{password_separated_by_underscores}

## Overview

| Property       | Detail                                                          |
| -------------- | --------------------------------------------------------------- |
| Organizer      | VishwaCTF                                                       |
| Year           | 2022                                                            |
| Category       | `Reverse`                                                       |
| Difficulty     | Easy 304/1000                                                   |
| Techniques     | `#anti-debugging` `#reversing`                                  |
| Challenge link | [Click me](https://ctf42.online/ctfs/vishwactf/2022/confusion/) |

## 1. Initial Reconnaissance

First, i tried to identification file using `Detect it Easy`, then i got this:

```text
PE64
Operation system: Windows (Vista) [AMD64, 64-bit]
Linker: Microsoft Linker (14.30.30706)
Compiler: Microsoft Visual C/C++ (19.30.30706) [LTCG/C++]
Language: C++
Library: Microsoft C/C++ Runtime [dynamic]
Tool: Microsoft Visual Studio (2022, 17.0)
Debug data: Records [CodeView, VC Feature, POGO]
(Heur) Debug data: Contains [Absolute PDB path]
```

Second, i running this program, then i got this:

```bash
You want see the rules? or continue to the challange?
( 'rules', 'continue' ) >

>> rules
------------------
----  RULES  -----
------------------

1. don't patch!
2. find the valid password.
3. make a keygen.
4. have fun! :)

>> continue
Input your username
> botnet
[1/11] Input your pass
> 1
[2/11] Input your pass
> 2
[3/11] Input your pass
> 3
[4/11] Input your pass
> 4
[5/11] Input your pass
> 5
[6/11] Input your pass
> 6
[7/11] Input your pass
> 7
[8/11] Input your pass
> 8
[9/11] Input your pass
> 9
[10/11] Input your pass
> 10
[11/11] Input your pass
> 11
Invalid password, try again!
```

It's means program get input 1 to 12, input 1 program require your name and then program require pass key.

## 2. Static Analysis

I used ghidra to get pseudocode like this:

### 2.1 main (`FUN_140001300`)

This function handle welcome program, you can see like this:

```bash
You want see the rules? or continue to the challange?
( 'rules', 'continue' ) >
```

```c++

void FUN_140001300(void)

{
  code *pcVar1;
  longlong ****pppplVar2;
  size_t sVar3;
  ulonglong uVar4;
  BOOL BVar5;
  HANDLE pvVar6;
  HMODULE hModule;
  FARPROC pFVar7;
  INT_PTR IVar8;
  void *pvVar9;
  longlong lVar10;
  longlong ****pppplVar11;
  basic_ostream<> *pbVar12;
  char ****ppppcVar13;
  char *pcVar14;
  size_t sVar15;
  undefined8 in_R9;
  undefined1 auStack_98 [32];
  undefined8 local_78;
  BOOL local_68 [2];
  longlong ****local_60 [2];
  size_t local_50;
  ulonglong local_48;
  char ****local_40 [2];
  ulonglong local_30;
  ulonglong local_28;
  ulonglong local_20;

  local_20 = DAT_140007008 ^ (ulonglong)auStack_98;
  FUN_1400015c0();
  FUN_1400015c0();
  FUN_1400015c0();
  FUN_140001950();
  FUN_140001ce0();
  local_50 = 0;
  local_48 = 0xf;
  local_60[0] = (longlong ****)0x0;
  local_30 = 0;
  local_28 = 0xf;
  local_40[0] = (char ****)0x0;
  local_68[0] = 0;
  pvVar6 = GetCurrentProcess();
  BVar5 = CheckRemoteDebuggerPresent(pvVar6,local_68);
  if ((BVar5 == 0) || (local_68[0] == 0)) {
    BVar5 = IsDebuggerPresent();
    if (BVar5 == 0) {
      hModule = LoadLibraryW(L"ntdll.dll");
      if (hModule != (HMODULE)0x0) {
        pFVar7 = GetProcAddress(hModule,"NtQueryInformationProcess");
        if (pFVar7 != (FARPROC)0x0) {
          pvVar6 = GetCurrentProcess();
          local_78 = 0;
          in_R9 = 4;
          IVar8 = (*pFVar7)(pvVar6,7,local_68);
          if (((int)IVar8 == 0) && (local_68[0] != 0)) goto LAB_140001597;
        }
      }
      FUN_140002660((basic_ostream<> *)cout_exref,"");
      FUN_140002660((basic_ostream<> *)cout_exref,"\t\t");
      FUN_140002660((basic_ostream<> *)cout_exref,"\t\t");
      FUN_140002660((basic_ostream<> *)cout_exref,"\t\t");
      FUN_140002660((basic_ostream<> *)cout_exref,
                    "You want see the rules? or continue to the challange?\n");
      do {
        FUN_140002660((basic_ostream<> *)cout_exref,"( \'rules\', \'continue\' ) > ");
        FUN_140002a90((basic_istream<> *)cin_exref,(longlong *)local_60);
        std::basic_ostream<>::operator<<((basic_ostream<> *)cout_exref,FUN_140002830);
        uVar4 = local_48;
        sVar3 = local_50;
        pppplVar2 = local_60[0];
        pppplVar11 = (longlong ****)local_60;
        if (0xf < local_48) {
          pppplVar11 = local_60[0];
        }
        if (local_50 == 0) {
LAB_1400014de:
          lVar10 = -1;
        }
        else {
          pvVar9 = memchr(pppplVar11,0x72,local_50);
          if (pvVar9 == (void *)0x0) goto LAB_1400014de;
          lVar10 = (longlong)pvVar9 - (longlong)pppplVar11;
        }
        pcVar14 = "rules\'?\n\n";
        if (lVar10 != 0) {
          pcVar14 = "continue\'?\n\n";
        }
        sVar15 = 0xffffffffffffffff;
        do {
          sVar15 = sVar15 + 1;
        } while (pcVar14[sVar15] != '\0');
        ppppcVar13 = (char ****)local_40;
        FUN_1400023f0((longlong *)ppppcVar13,pcVar14,sVar15);
        pppplVar11 = (longlong ****)local_60;
        if (0xf < uVar4) {
          pppplVar11 = pppplVar2;
        }
        if (((sVar3 == 5) && (*(int *)pppplVar11 == 0x656c7572)) &&
           (*(char *)((longlong)pppplVar11 + 4) == 's')) {
          FUN_140002070();
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        pppplVar11 = (longlong ****)local_60;
        if (0xf < uVar4) {
          pppplVar11 = pppplVar2;
        }
        if ((sVar3 == 8) && (*pppplVar11 == (longlong ***)0x65756e69746e6f63)) {
          FUN_140002120(ppppcVar13,pcVar14,sVar15,in_R9);
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        pbVar12 = FUN_140002660((basic_ostream<> *)cout_exref,"[!] Whoops, input again. ");
        pbVar12 = FUN_140002660(pbVar12,"did you mean -> \'");
        ppppcVar13 = (char ****)local_40;
        if (0xf < local_28) {
          ppppcVar13 = local_40[0];
        }
        FUN_140002c80(pbVar12,(char *)ppppcVar13,local_30);
      } while( true );
    }
  }
LAB_140001597:
  MessageBoxA((HWND)0x0,"A debugger has been founded running in the program. Please unload it.",
              "Whoops",0x10);
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```

### 2.2 rules `(FUN_140002070)`

This function handle rules choice

```c++
void FUN_140002070(void)

{
  system("cls");
  FUN_140002660((basic_ostream<> *)cout_exref,"------------------\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"----  RULES  -----\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"------------------\n\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"1. don\'t patch!\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"2. find the valid password.\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"3. make a keygen.\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"4. have fun! :)\n");
  system("pause");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

### 2.3 continue `(FUN_140002120)`

This function is a core of program, because handle user input to generate keygen

```c++

void FUN_140002120(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  BOOL BVar1;
  uint uVar2;
  uint uVar3;
  ushort *puVar4;
  uint *puVar5;
  bool bVar6;
  undefined1 auStack_a8 [32];
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined4 local_68;
  longlong local_60;
  undefined8 uStack_58;
  ulonglong local_50;
  undefined8 uStack_48;
  uint local_40;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  ulonglong local_10;

  local_10 = DAT_140007008 ^ (ulonglong)auStack_a8;
  local_68 = 0;
  BVar1 = IsDebuggerPresent();
  if (BVar1 != 0) {
    MessageBoxA((HWND)0x0,"A debugger has been founded running in the program. Please unload it.",
                "Whoops",0x10);
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  system("cls");
  local_50 = 0;
  uStack_48 = 0xf;
  local_60 = 0;
  local_68 = 1;
  FUN_140002660((basic_ostream<> *)cout_exref,"Input your username\n");
  FUN_140002660((basic_ostream<> *)cout_exref,"> ");
  FUN_140002a90((basic_istream<> *)cin_exref,&local_60);
  local_88 = 0xff9cffa0ff98ffb1;
  local_78 = CONCAT26(local_78._6_2_,0xffffffb2ffe2);
  uStack_80 = 0xffe0ffa2ff99ffb8;
  uVar2 = 0;
  puVar4 = (ushort *)&local_88;
  do {
    *puVar4 = ~(*puVar4 - (ushort)uVar2) ^ (ushort)uVar2;
    uVar2 = uVar2 + 1;
    puVar4 = puVar4 + 1;
  } while (uVar2 < 0xb);
  uVar2 = 0;
  puVar5 = &local_40;
  do {
    uVar2 = uVar2 + 1;
    FUN_140001020("[%d/11] Input your pass\n",(ulonglong)uVar2,param_3,param_4);
    FUN_140002660((basic_ostream<> *)cout_exref,"> ");
    std::basic_istream<>::operator>>((basic_istream<> *)cin_exref,(int *)puVar5);
    puVar5 = puVar5 + 1;
  } while ((int)uVar2 < 0xb);
  bVar6 = local_40 == ((ushort)local_88 ^ (uint)local_50);
  uVar2 = bVar6 + 1;
  if (local_3c != (local_88._2_2_ ^ (uint)local_50)) {
    uVar2 = (uint)bVar6;
  }
  uVar3 = uVar2 + 1;
  if (local_38 != (local_88._4_2_ ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
  uVar2 = uVar3 + 1;
  if (local_34 != (local_88._6_2_ ^ (uint)local_50)) {
    uVar2 = uVar3;
  }
  uVar3 = uVar2 + 1;
  if (local_30 != ((ushort)uStack_80 ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
  uVar2 = uVar3 + 1;
  if (local_2c != (uStack_80._2_2_ ^ (uint)local_50)) {
    uVar2 = uVar3;
  }
  uVar3 = uVar2 + 1;
  if (local_28 != (uStack_80._4_2_ ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
  uVar2 = uVar3 + 1;
  if (local_24 != (uStack_80._6_2_ ^ (uint)local_50)) {
    uVar2 = uVar3;
  }
  uVar3 = uVar2 + 1;
  if (local_20 != ((ushort)local_78 ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
  uVar2 = uVar3 + 1;
  if (local_1c != (local_78._2_2_ ^ (uint)local_50)) {
    uVar2 = uVar3;
  }
  uVar3 = uVar2 + 1;
  if (local_18 != (local_78._4_2_ ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
  if (uVar3 == 0xb) {
    local_88 = local_60;
    uStack_80 = uStack_58;
    local_78 = local_50;
    uStack_70 = uStack_48;
    FUN_140001020("Well done,    %s. Now submit the flag       \n",&local_88,(ulonglong)uVar2,
                  local_50 & 0xffffffff);
    system("pause");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  FUN_140002660((basic_ostream<> *)cout_exref,"Invalid password, try again!\n");
  system("pause");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

On the `continue` function i got anti debugger program, this will be run when program detect you using debugger after reach to this part:

```c++
 BVar1 = IsDebuggerPresent();
  if (BVar1 != 0) {
    MessageBoxA((HWND)0x0,"A debugger has been founded running in the program. Please unload it.",
                "Whoops",0x10);
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
```

this password have 3 constant value to make key, like this:

```c++
local_88 = 0xff9cffa0ff98ffb1;
local_78 = CONCAT26(local_78._6_2_,0xffffffb2ffe2);
uStack_80 = 0xffe0ffa2ff99ffb8;
```

and this key set to 16 bytes (hexadecimal)

```c++
puVar4 = (ushort *)&local_88;
```

Keys will be generate like this in every loop:

```c++
 *puVar4 = ~(*puVar4 - (ushort)uVar2) ^ (ushort)uVar2;
```

and xor again with username length, username value stored in `local_50` when intialize `0` in earlier

```c++
  if (local_38 != (local_88._4_2_ ^ (uint)local_50)) {
    uVar3 = uVar2;
  }
```

## 3. Solution

First, i build a script to generate key, like this:

```c++
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define KEY_COUNT 11
#define USERNAME "nLYTCmdXobFRhs"

uint16_t transform_value(uint16_t value, uint16_t index, size_t username_length)
{

    uint16_t result = ~(value - index);

    result = result ^ index;

    result = result ^ username_length;

    return result;
}

void generate_key(uint16_t values[], uint16_t keys[], size_t username_length)
{
    for (int i = 0; i < KEY_COUNT; i++)
    {
        keys[i] = transform_value(values[i], i, username_length);
    };
}

int main()
{
    uint16_t bytes[KEY_COUNT] = {
        0xffb1, 0xff98, 0xffa0, 0xff9c, 0xffb8, 0xff99, 0xffa2, 0xffe0, 0xffe2, 0xffb2, 0xffff};

    uint16_t keys[KEY_COUNT];

    generate_key(bytes, keys , strlen(USERNAME));

    for (int i = 0; i < KEY_COUNT; i++)
    {
        printf("[%i/11] %i\n", i + 1, keys[i]);
    }
}
```

Output:

```bash
[1/11] 64
[2/11] 103
[3/11] 109
[4/11] 107
[5/11] 65
[6/11] 96
[7/11] 107
[8/11] 47
[9/11] 35
[10/11] 81
[11/11] 14
```

Second, input key one by one:

```bash
> Confusion.exe

Input your username
> nLYTCmdXobFRhs
[1/11] Input your pass
> 64
[2/11] Input your pass
> 103
[3/11] Input your pass
> 109
[4/11] Input your pass
> 107
[5/11] Input your pass
> 65
[6/11] Input your pass
> 96
[7/11] Input your pass
> 107
[8/11] Input your pass
> 47
[9/11] Input your pass
> 35
[10/11] Input your pass
> 81
[11/11] Input your pass
> 14
Well done,    nLYTCmdXobFRhs. Now submit the flag
```

**Flag**: `vishwaCTF{64_103_109_107_65_96_107_47_35_81_14}`
